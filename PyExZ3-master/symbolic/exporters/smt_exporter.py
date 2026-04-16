import json
import os
import re
import time
from hashlib import sha256

from ..symbolic_types import SymbolicBool, SymbolicFloat, SymbolicStr


class SMTExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _split_top_level(self, expr_str):
        parts = []
        current = []
        depth = 0
        in_string = False
        escape = False

        for char in expr_str:
            if in_string:
                current.append(char)
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
                current.append(char)
            elif char == "(":
                depth += 1
                current.append(char)
            elif char == ")":
                depth -= 1
                current.append(char)
            elif char.isspace() and depth == 0:
                if current:
                    parts.append("".join(current))
                    current = []
            else:
                current.append(char)

        if current:
            parts.append("".join(current))

        return parts

    def _parse_symbolic_expr(self, expr_str):
        expr_str = expr_str.strip()
        if not expr_str:
            return expr_str

        if expr_str == "True":
            return "true"
        if expr_str == "False":
            return "false"
        if re.fullmatch(r"-?\d+(\.\d+)?", expr_str):
            return expr_str
        if expr_str.startswith('"') and expr_str.endswith('"'):
            return expr_str

        if expr_str.startswith("(") and expr_str.endswith(")"):
            inner = expr_str[1:-1].strip()
            parts = self._split_top_level(inner)
            if not parts:
                return expr_str

            op = parts[0]
            args = parts[1:]

            binary_map = {
                "<": "<",
                ">": ">",
                "<=": "<=",
                ">=": ">=",
                "==": "=",
                "+": "+",
                "*": "*",
                "/": "/",
                "%": "mod",
                "mod": "mod",
                "and": "and",
                "or": "or",
                "xor": "xor",
            }

            if op == "not" and len(args) == 1:
                return f"(not {self._parse_symbolic_expr(args[0])})"
            if op == "!=" and len(args) == 2:
                return f"(not (= {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])}))"
            if op == "abs" and len(args) == 1:
                return f"(abs {self._parse_symbolic_expr(args[0])})"
            if op == "-" and len(args) == 1:
                return f"(- {self._parse_symbolic_expr(args[0])})"
            if op in binary_map and len(args) == 2:
                return f"({binary_map[op]} {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"

        return expr_str

    def _convert_predicate_to_smt(self, predicate, force_result=None):
        symbolic_expr = predicate.get_symbolic_expr() if hasattr(predicate, "get_symbolic_expr") else str(predicate)
        smt_expr = self._parse_symbolic_expr(symbolic_expr)
        result = predicate.result if force_result is None else force_result
        return smt_expr if result else f"(not {smt_expr})"

    def _infer_sort(self, symbolic_value):
        if isinstance(symbolic_value, SymbolicBool):
            return "Bool"
        if isinstance(symbolic_value, SymbolicFloat):
            return "Real"
        if isinstance(symbolic_value, SymbolicStr):
            return "String"
        return "Int"

    def _extract_variables(self, predicates, query):
        variables = {}
        ignored = {"se", "const"}

        def remember(symbolic_value):
            name = getattr(symbolic_value, "name", None)
            if not name or name in ignored:
                return
            sort = self._infer_sort(symbolic_value)
            if name not in variables or variables[name] == "Int":
                variables[name] = sort

        def walk(expr):
            if expr is None:
                return
            if isinstance(expr, list):
                for item in expr[1:]:
                    walk(item)
                return
            if hasattr(expr, "symtype"):
                walk(expr.symtype)
                return
            if hasattr(expr, "isVariable") and callable(expr.isVariable):
                if expr.isVariable():
                    remember(expr)
                else:
                    walk(getattr(expr, "expr", None))
                return
            if hasattr(expr, "expr") and getattr(expr, "expr", None) is not None:
                walk(expr.expr)

        for predicate in predicates:
            walk(predicate)
        if query is not None:
            walk(query)

        return [(name, variables[name]) for name in sorted(variables)]

    def _generate_path_id(self, predicates, query=None, negate_query=False):
        expressions = []
        for predicate in predicates:
            if hasattr(predicate, "get_symbolic_expr"):
                expressions.append(f"{predicate.get_symbolic_expr()}:{predicate.result}")

        if query and hasattr(query, "get_symbolic_expr"):
            expressions.append(f"query:{query.get_symbolic_expr()}:{query.result}:{negate_query}")

        expressions.sort()
        return sha256("".join(expressions).encode()).hexdigest()[:16]

    def _build_smt_content(self, solver, predicates, variables, query=None, negate_query=False, comment_prefix="Path"):
        solver_name = getattr(solver, "name", solver.__class__.__name__ if solver else "unknown")
        path_id = self._generate_path_id(predicates, query, negate_query=negate_query)

        smt_content = "(set-logic ALL)\n"
        smt_content += f"; {comment_prefix} ID: {path_id}\n"
        smt_content += f"; Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        smt_content += f"; Solver: {solver_name}\n"
        smt_content += f"; Number of predicates: {len(predicates)}\n"
        smt_content += f"; Has query: {bool(query)}\n\n"

        for name, sort in variables:
            smt_content += f"(declare-const {name} {sort})\n"
        smt_content += "\n"

        for predicate in predicates:
            symbolic_expr = predicate.get_symbolic_expr() if hasattr(predicate, "get_symbolic_expr") else str(predicate)
            smt_content += f"; ({symbolic_expr}) ({predicate.result})\n"
            smt_content += f"(assert {self._convert_predicate_to_smt(predicate)})\n"
        smt_content += "\n"

        if query is not None:
            symbolic_expr = query.get_symbolic_expr() if hasattr(query, "get_symbolic_expr") else str(query)
            query_expr = self._convert_predicate_to_smt(query)
            smt_content += f"; Query: ({symbolic_expr}) ({query.result})\n"
            if negate_query:
                smt_content += f"(assert (not {query_expr}))\n\n"
            else:
                smt_content += f"(assert {query_expr})\n\n"

        smt_content += "(check-sat)\n"
        smt_content += "(get-model)\n"
        return path_id, solver_name, smt_content

    def export_executed_path(self, solver, predicates):
        predicates = list(predicates)
        variables = self._extract_variables(predicates, None)
        path_id, solver_name, smt_content = self._build_smt_content(
            solver,
            predicates,
            variables,
            comment_prefix="Executed Path",
        )

        smt_file = os.path.join(self.output_dir, f"path_{path_id}.smt2")
        with open(smt_file, "w", encoding="utf-8") as file_obj:
            file_obj.write(smt_content)
        with open(os.path.join(self.output_dir, "path.smt2"), "w", encoding="utf-8") as file_obj:
            file_obj.write(smt_content)

        metadata = {
            "path_id": path_id,
            "timestamp": time.time(),
            "solver": solver_name,
            "predicates_count": len(predicates),
            "has_query": False,
            "variables": [name for name, _ in variables],
            "smt_file": os.path.basename(smt_file),
            "mode": "executed_path",
        }
        with open(os.path.join(self.output_dir, f"path_{path_id}.json"), "w", encoding="utf-8") as file_obj:
            json.dump(metadata, file_obj, indent=2)

    def export_query_path(self, solver, asserts, query):
        predicates = list(reversed(list(asserts)))
        variables = self._extract_variables(predicates, query)
        path_id, solver_name, smt_content = self._build_smt_content(
            solver,
            predicates,
            variables,
            query=query,
            negate_query=True,
            comment_prefix="Frontier Constraint",
        )

        smt_file = os.path.join(self.output_dir, f"path_{path_id}.smt2")
        with open(smt_file, "w", encoding="utf-8") as file_obj:
            file_obj.write(smt_content)

        metadata = {
            "path_id": path_id,
            "timestamp": time.time(),
            "solver": solver_name,
            "assertions_count": len(predicates),
            "has_query": bool(query),
            "variables": [name for name, _ in variables],
            "smt_file": os.path.basename(smt_file),
            "mode": "frontier_query",
        }
        with open(os.path.join(self.output_dir, f"path_{path_id}.json"), "w", encoding="utf-8") as file_obj:
            json.dump(metadata, file_obj, indent=2)

    def export_frontier(self, solver, frontier):
        frontier_dir = os.path.join(self.output_dir, "frontier")
        os.makedirs(frontier_dir, exist_ok=True)

        frontier_summary = []

        for index, constraint in enumerate(frontier):
            asserts, query = constraint.getAssertsAndQuery()
            predicates = list(reversed(list(asserts)))
            variables = self._extract_variables(predicates, query)
            path_id, _, smt_content = self._build_smt_content(
                solver,
                predicates,
                variables,
                query=query,
                negate_query=True,
                comment_prefix="Frontier Constraint",
            )

            smt_file = os.path.join(frontier_dir, f"frontier_{index}_{path_id}.smt2")
            with open(smt_file, "w", encoding="utf-8") as file_obj:
                file_obj.write(smt_content)

            frontier_summary.append({
                "constraint_id": path_id,
                "index": index,
                "assertions_count": len(predicates),
                "has_query": bool(query),
                "variables_count": len(variables),
                "smt_file": os.path.basename(smt_file),
            })

        with open(os.path.join(frontier_dir, "frontier_summary.json"), "w", encoding="utf-8") as file_obj:
            json.dump(frontier_summary, file_obj, indent=2)

    def export_execution_summary(self, execution_data):
        smt_content = "(set-logic ALL)\n"
        smt_content += "; Execution Summary\n"
        smt_content += f"; Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        smt_content += f"; Generated Inputs: {len(execution_data.get('generated_inputs', []))}\n"
        smt_content += f"; Return Values: {execution_data.get('return_values', [])}\n"
        smt_content += f"; Path Length: {len(execution_data.get('branch_trace', []))}\n"

        with open(os.path.join(self.output_dir, "execution_summary.smt2"), "w", encoding="utf-8") as file_obj:
            file_obj.write(smt_content)

        execution_summary = {
            "timestamp": time.time(),
            "generated_inputs_count": len(execution_data.get('generated_inputs', [])),
            "return_values": execution_data.get('return_values', []),
            "path_length": len(execution_data.get('branch_trace', [])),
            "branch_trace": execution_data.get('branch_trace', []),
        }

        with open(os.path.join(self.output_dir, "execution_summary.json"), "w", encoding="utf-8") as file_obj:
            json.dump(execution_summary, file_obj, indent=2)
