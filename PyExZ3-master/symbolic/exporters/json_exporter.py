import json
import os
import time

from ..normalizer import ConstraintNormalizer


class JSONExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_concrete_value(self, value):
        """Get concrete value from symbolic type."""
        if hasattr(value, "getConcrValue"):
            return value.getConcrValue()
        if isinstance(value, dict):
            return {key: self._get_concrete_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._get_concrete_value(item) for item in value]
        return value

    def _extract_semantic_tags(self, predicate):
        """Extract semantic tags from predicate."""
        tags = []

        sym_type = predicate.symtype
        if hasattr(sym_type, "__class__"):
            tags.append(f"type:{sym_type.__class__.__name__}")

        expr = getattr(sym_type, "expr", None)
        if isinstance(expr, list) and expr:
            tags.append(f"op:{expr[0]}")

        tags.append(f"branch:{predicate.result}")

        if predicate.source_file and predicate.source_line:
            tags.append(f"loc:{predicate.source_file}:{predicate.source_line}")

        return tags

    def _unique_variables(self, predicate):
        return sorted(set(predicate.getVars()))

    def _build_constraint_templates(self, predicates, raw_predicates, normalized_predicates):
        templates = []
        for predicate, raw, normalized in zip(predicates, raw_predicates, normalized_predicates):
            expr = getattr(predicate.symtype, "expr", None)
            operation = expr[0] if isinstance(expr, list) and expr else None
            templates.append(
                {
                    "raw": raw,
                    "normalized": normalized,
                    "operation": operation,
                    "variables": self._unique_variables(predicate),
                }
            )
        return templates

    def _build_branch_location_sequence(self, predicates):
        sequence = []
        for predicate in predicates:
            sequence.append(
                {
                    "source_file": predicate.source_file,
                    "source_line": predicate.source_line,
                    "source_col": getattr(predicate, "source_col", 0),
                    "branch_id": predicate.branch_id,
                }
            )
        return sequence

    def _build_variable_participation_graph(self, predicates):
        all_variables = []
        seen = set()
        for predicate in predicates:
            for variable in self._unique_variables(predicate):
                if variable not in seen:
                    seen.add(variable)
                    all_variables.append(variable)

        graph = {"nodes": all_variables, "edges": []}
        for index, predicate in enumerate(predicates):
            variables = self._unique_variables(predicate)
            for left_index in range(len(variables)):
                for right_index in range(left_index + 1, len(variables)):
                    graph["edges"].append(
                        {
                            "source": variables[left_index],
                            "target": variables[right_index],
                            "predicate_index": index,
                            "predicate": predicate.get_symbolic_expr(),
                        }
                    )
        return graph

    def _build_path_summary_vector(self, predicates):
        all_variables = set()
        for predicate in predicates:
            all_variables.update(predicate.getVars())

        denominator = len(predicates) + 1
        return {
            "path_length": len(predicates),
            "num_variables": len(all_variables),
            "num_branches": len([predicate for predicate in predicates if predicate.result]),
            "num_negations": len([predicate for predicate in predicates if not predicate.result]),
            "branch_diversity": len(set(predicate.get_symbolic_expr() for predicate in predicates)),
            "variable_density": len(all_variables) / denominator,
            "predicate_complexity": sum(len(str(predicate.get_symbolic_expr())) for predicate in predicates) / denominator,
            "branch_balance": len([predicate for predicate in predicates if predicate.result]) / denominator,
        }

    def _build_standardized_features(self, predicates, raw_predicates, normalized_predicates):
        return {
            "normalized_pc": normalized_predicates,
            "branch_trace": [predicate.to_dict() for predicate in predicates],
            "semantic_tags": [self._extract_semantic_tags(predicate) for predicate in predicates],
            "source_spans": [
                (
                    predicate.source_file,
                    predicate.source_line,
                    getattr(predicate, "source_col", 0),
                    predicate.branch_id,
                )
                for predicate in predicates
                if predicate.source_file and predicate.source_line
            ],
            "path_summary": {
                "path_length": len(predicates),
                "num_variables": len(set(variable for predicate in predicates for variable in predicate.getVars())),
                "num_branches": len([predicate for predicate in predicates if predicate.result]),
                "num_negations": len([predicate for predicate in predicates if not predicate.result]),
            },
            "exception_profile": {
                "has_exceptions": False,
                "exception_types": [],
            },
            "path_predicate_sequence": [predicate.get_symbolic_expr() for predicate in predicates],
            "normalized_constraint_templates": self._build_constraint_templates(
                predicates, raw_predicates, normalized_predicates
            ),
            "branch_location_sequence": self._build_branch_location_sequence(predicates),
            "variable_participation_graph": self._build_variable_participation_graph(predicates),
            "path_summary_vector": self._build_path_summary_vector(predicates),
        }

    def _build_path_data(self, path_key, path_value, predicates, inputs, return_value):
        normalizer = ConstraintNormalizer()
        raw_predicates, normalized_predicates = normalizer.normalize_path(predicates)
        standardized_features = self._build_standardized_features(
            predicates, raw_predicates, normalized_predicates
        )

        semantic_info = {
            "path_length": len(predicates),
            "branch_directions": [predicate.result for predicate in predicates],
            "semantic_tags": [self._extract_semantic_tags(predicate) for predicate in predicates],
            "symbolic_variables": list(set(variable for predicate in predicates for variable in predicate.getVars())),
            "source_locations": [
                (predicate.source_file, predicate.source_line, predicate.branch_id)
                for predicate in predicates
                if predicate.source_file and predicate.source_line
            ],
        }

        path_data = {
            path_key: path_value,
            "timestamp": time.time(),
            "input_model": {
                key: value.toString() if hasattr(value, "toString") else str(value)
                for key, value in inputs.items()
            },
            "concrete_inputs": {key: self._get_concrete_value(value) for key, value in inputs.items()},
            "return_value": return_value,
            "branch_trace": standardized_features["branch_trace"],
            "path_predicates_raw": raw_predicates,
            "path_predicates_normalized": normalized_predicates,
            "semantic_info": semantic_info,
            "path_constraints": {
                "assertions": [predicate.get_symbolic_expr() for predicate in predicates if predicate.result],
                "negations": [predicate.get_symbolic_expr() for predicate in predicates if not predicate.result],
            },
            "standardized_features": standardized_features,
        }
        return path_data

    def export_path(self, path, inputs, return_values):
        """Export path information to JSON."""
        current_path = path.get_current_path()
        path_data = self._build_path_data(
            "path_id",
            id(path),
            current_path,
            inputs,
            return_values[-1] if return_values else None,
        )

        with open(os.path.join(self.output_dir, "path.json"), "w", encoding="utf-8") as file_obj:
            json.dump(path_data, file_obj, indent=2, default=str)

        return path_data

    def export_frontier(self, frontier):
        """Export frontier constraints to JSON."""
        frontier_dir = os.path.join(self.output_dir, "frontier")
        os.makedirs(frontier_dir, exist_ok=True)

        frontier_summary = []
        normalizer = ConstraintNormalizer()

        for index, constraint in enumerate(frontier):
            path_predicates = constraint.get_path_predicates()
            _, normalized_predicates = normalizer.normalize_path(path_predicates)

            semantic_info = {
                "path_length": len(path_predicates),
                "branch_directions": [predicate.result for predicate in path_predicates],
                "semantic_tags": [self._extract_semantic_tags(predicate) for predicate in path_predicates],
                "symbolic_variables": list(
                    set(variable for predicate in path_predicates for variable in predicate.getVars())
                ),
            }

            frontier_data = {
                "constraint_id": constraint.id,
                "timestamp": time.time(),
                "path_predicates": [predicate.to_dict() for predicate in path_predicates],
                "path_predicates_raw": [predicate.get_symbolic_expr() for predicate in path_predicates],
                "path_predicates_normalized": normalized_predicates,
                "inputs": {key: self._get_concrete_value(value) for key, value in constraint.inputs.items()},
                "semantic_info": semantic_info,
                "processed": constraint.processed,
            }

            with open(
                os.path.join(frontier_dir, f"frontier_{index}.json"),
                "w",
                encoding="utf-8",
            ) as file_obj:
                json.dump(frontier_data, file_obj, indent=2, default=str)

            frontier_summary.append(
                {
                    "constraint_id": constraint.id,
                    "path_length": len(path_predicates),
                    "processed": constraint.processed,
                    "variables": semantic_info["symbolic_variables"],
                }
            )

        with open(
            os.path.join(frontier_dir, "frontier_summary.json"),
            "w",
            encoding="utf-8",
        ) as file_obj:
            json.dump(frontier_summary, file_obj, indent=2)

    def export_execution_summary(self, execution_data):
        """Export execution summary to JSON."""
        summary_data = {
            "timestamp": time.time(),
            "generated_inputs": execution_data.get("generated_inputs", []),
            "return_values": execution_data.get("return_values", []),
            "execution_count": len(execution_data.get("generated_inputs", [])),
            "path_lengths": execution_data.get("path_lengths", []),
            "semantic_summary": {
                "total_branches": sum(len(trace) for trace in execution_data.get("branch_traces", [])),
                "unique_variables": list(
                    set(
                        variable
                        for trace in execution_data.get("branch_traces", [])
                        for predicate in trace
                        for variable in predicate.getVars()
                    )
                ),
            },
        }

        with open(
            os.path.join(self.output_dir, "execution_summary.json"),
            "w",
            encoding="utf-8",
        ) as file_obj:
            json.dump(summary_data, file_obj, indent=2, default=str)

    def export_branch_trace(self, branch_trace):
        """Export branch trace to JSON."""
        trace_data = {
            "timestamp": time.time(),
            "trace_length": len(branch_trace),
            "branches": [
                {
                    "predicate": predicate.get_symbolic_expr(),
                    "result": predicate.result,
                    "source_file": predicate.source_file,
                    "source_line": predicate.source_line,
                    "branch_id": predicate.branch_id,
                    "semantic_tags": self._extract_semantic_tags(predicate),
                }
                for predicate in branch_trace
            ],
        }

        with open(
            os.path.join(self.output_dir, "branch_trace.json"),
            "w",
            encoding="utf-8",
        ) as file_obj:
            json.dump(trace_data, file_obj, indent=2, default=str)

    def export_semantic_tags(self, path):
        """Export semantic tags to JSON."""
        current_path = path.get_current_path()

        tags_data = {
            "timestamp": time.time(),
            "total_tags": sum(len(self._extract_semantic_tags(predicate)) for predicate in current_path),
            "per_branch_tags": [
                {
                    "branch_index": index,
                    "predicate": predicate.get_symbolic_expr(),
                    "tags": self._extract_semantic_tags(predicate),
                }
                for index, predicate in enumerate(current_path)
            ],
        }

        with open(
            os.path.join(self.output_dir, "semantic_tags.json"),
            "w",
            encoding="utf-8",
        ) as file_obj:
            json.dump(tags_data, file_obj, indent=2, default=str)

    def export_all_executions(self, symbolic_inputs_list, return_values, branch_traces_list):
        """Export all executions to separate files."""
        executions_dir = os.path.join(self.output_dir, "executions")
        os.makedirs(executions_dir, exist_ok=True)

        for execution_id, (symbolic_inputs, return_value, branch_trace) in enumerate(
            zip(symbolic_inputs_list, return_values, branch_traces_list)
        ):
            execution_dir = os.path.join(executions_dir, f"execution_{execution_id}")
            os.makedirs(execution_dir, exist_ok=True)

            execution_exporter = JSONExporter(execution_dir)
            path_data = execution_exporter._build_path_data(
                "execution_id",
                execution_id,
                branch_trace,
                symbolic_inputs,
                return_value,
            )

            with open(os.path.join(execution_dir, "path.json"), "w", encoding="utf-8") as file_obj:
                json.dump(path_data, file_obj, indent=2, default=str)

            trace_data = {
                "timestamp": time.time(),
                "trace_length": len(branch_trace),
                "branches": [
                    {
                        "predicate": predicate.get_symbolic_expr(),
                        "result": predicate.result,
                        "source_file": predicate.source_file,
                        "source_line": predicate.source_line,
                        "branch_id": predicate.branch_id,
                        "semantic_tags": execution_exporter._extract_semantic_tags(predicate),
                    }
                    for predicate in branch_trace
                ],
            }

            with open(
                os.path.join(execution_dir, "branch_trace.json"),
                "w",
                encoding="utf-8",
            ) as file_obj:
                json.dump(trace_data, file_obj, indent=2, default=str)

            tags_data = {
                "timestamp": time.time(),
                "total_tags": sum(
                    len(execution_exporter._extract_semantic_tags(predicate))
                    for predicate in branch_trace
                ),
                "per_branch_tags": [
                    {
                        "branch_index": index,
                        "predicate": predicate.get_symbolic_expr(),
                        "tags": execution_exporter._extract_semantic_tags(predicate),
                    }
                    for index, predicate in enumerate(branch_trace)
                ],
            }

            with open(
                os.path.join(execution_dir, "semantic_tags.json"),
                "w",
                encoding="utf-8",
            ) as file_obj:
                json.dump(tags_data, file_obj, indent=2, default=str)
