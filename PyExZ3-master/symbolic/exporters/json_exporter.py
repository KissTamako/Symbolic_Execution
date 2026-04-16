import json
import os
import time
from ..normalizer import ConstraintNormalizer

class JSONExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _get_concrete_value(self, value):
        """Get concrete value from symbolic type"""
        if hasattr(value, 'getConcrValue'):
            return value.getConcrValue()
        elif isinstance(value, dict):
            return {k: self._get_concrete_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [self._get_concrete_value(item) for item in value]
        return value
    
    def _extract_semantic_tags(self, predicate):
        """Extract semantic tags from predicate"""
        tags = []
        
        # Add type-based tags
        sym_type = predicate.symtype
        if hasattr(sym_type, '__class__'):
            tags.append(f"type:{sym_type.__class__.__name__}")
        
        # Add operation-based tags
        if hasattr(sym_type, 'expr') and sym_type.expr:
            if isinstance(sym_type.expr, list) and len(sym_type.expr) > 0:
                op = sym_type.expr[0]
                tags.append(f"op:{op}")
        
        # Add branch direction tag
        tags.append(f"branch:{predicate.result}")
        
        # Add location tag if available
        if predicate.source_file and predicate.source_line:
            tags.append(f"loc:{predicate.source_file}:{predicate.source_line}")
        
        return tags
    
    def export_path(self, path, inputs, return_values):
        """Export path information to JSON"""
        current_path = path.get_current_path()
        
        # 规范化路径约束
        normalizer = ConstraintNormalizer()
        raw_predicates, normalized_predicates = normalizer.normalize_path(current_path)
        
        # Extract semantic information
        semantic_info = {
            "path_length": len(current_path),
            "branch_directions": [p.result for p in current_path],
            "semantic_tags": [self._extract_semantic_tags(p) for p in current_path],
            "symbolic_variables": list(set(var for p in current_path for var in p.getVars())),
            "source_locations": [(p.source_file, p.source_line, p.branch_id) for p in current_path if p.source_file and p.source_line]
        }
        
        # 构建标准化的特征输出
        standardized_features = {
            "normalized_pc": normalized_predicates,  # 归一化的路径条件
            "branch_trace": [p.to_dict() for p in current_path],  # 分支跟踪
            "semantic_tags": [self._extract_semantic_tags(p) for p in current_path],  # 语义标签
            "source_spans": [(p.source_file, p.source_line, getattr(p, 'source_col', 0), p.branch_id) for p in current_path if p.source_file and p.source_line],  # 源码位置
            "path_summary": {
                "path_length": len(current_path),
                "num_variables": len(set(var for p in current_path for var in p.getVars())),
                "num_branches": len([p for p in current_path if p.result]),
                "num_negations": len([p for p in current_path if not p.result])
            },  # 路径摘要
            "exception_profile": {
                "has_exceptions": False,  # 暂时设为 False，后续可以根据实际情况修改
                "exception_types": []
            }  # 异常概况
        }
        
        path_data = {
            "path_id": id(path),
            "timestamp": time.time(),
            "input_model": {k: v.toString() if hasattr(v, 'toString') else str(v) for k, v in inputs.items()},
            "concrete_inputs": {k: self._get_concrete_value(v) for k, v in inputs.items()},
            "return_value": return_values[-1] if return_values else None,
            "branch_trace": standardized_features["branch_trace"],
            "path_predicates_raw": [p.get_symbolic_expr() for p in current_path],
            "path_predicates_normalized": normalized_predicates,
            "semantic_info": semantic_info,
            "path_constraints": {
                "assertions": [p.get_symbolic_expr() for p in current_path if p.result],
                "negations": [p.get_symbolic_expr() for p in current_path if not p.result]
            },
            "standardized_features": standardized_features  # 添加标准化特征输出
        }
        
        with open(os.path.join(self.output_dir, "path.json"), "w") as f:
            json.dump(path_data, f, indent=2, default=str)
        
        return path_data
    
    def export_frontier(self, frontier):
        """Export frontier constraints to JSON"""
        frontier_dir = os.path.join(self.output_dir, "frontier")
        os.makedirs(frontier_dir, exist_ok=True)
        
        frontier_summary = []
        
        # 创建约束规范化器
        normalizer = ConstraintNormalizer()
        
        for i, constraint in enumerate(frontier):
            path_predicates = constraint.get_path_predicates()
            
            # 规范化路径约束
            raw_predicates, normalized_predicates = normalizer.normalize_path(path_predicates)
            
            # Extract semantic information for each frontier constraint
            semantic_info = {
                "path_length": len(path_predicates),
                "branch_directions": [p.result for p in path_predicates],
                "semantic_tags": [self._extract_semantic_tags(p) for p in path_predicates],
                "symbolic_variables": list(set(var for p in path_predicates for var in p.getVars()))
            }
            
            frontier_data = {
                "constraint_id": constraint.id,
                "timestamp": time.time(),
                "path_predicates": [p.to_dict() for p in path_predicates],
                "path_predicates_raw": [p.get_symbolic_expr() for p in path_predicates],
                "path_predicates_normalized": normalized_predicates,
                "inputs": {k: self._get_concrete_value(v) for k, v in constraint.inputs.items()},
                "semantic_info": semantic_info,
                "processed": constraint.processed
            }
            
            with open(os.path.join(frontier_dir, f"frontier_{i}.json"), "w") as f:
                json.dump(frontier_data, f, indent=2, default=str)
            
            frontier_summary.append({
                "constraint_id": constraint.id,
                "path_length": len(path_predicates),
                "processed": constraint.processed,
                "variables": semantic_info["symbolic_variables"]
            })
        
        # Export frontier summary
        with open(os.path.join(frontier_dir, "frontier_summary.json"), "w") as f:
            json.dump(frontier_summary, f, indent=2)
    
    def export_execution_summary(self, execution_data):
        """Export execution summary to JSON"""
        summary_data = {
            "timestamp": time.time(),
            "generated_inputs": execution_data.get('generated_inputs', []),
            "return_values": execution_data.get('return_values', []),
            "execution_count": len(execution_data.get('generated_inputs', [])),
            "path_lengths": execution_data.get('path_lengths', []),
            "semantic_summary": {
                "total_branches": sum(len(trace) for trace in execution_data.get('branch_traces', [])),
                "unique_variables": list(set(var for trace in execution_data.get('branch_traces', []) 
                                          for p in trace for var in p.getVars()))
            }
        }
        
        with open(os.path.join(self.output_dir, "execution_summary.json"), "w") as f:
            json.dump(summary_data, f, indent=2, default=str)
    
    def export_branch_trace(self, branch_trace):
        """Export branch trace to JSON"""
        trace_data = {
            "timestamp": time.time(),
            "trace_length": len(branch_trace),
            "branches": [{
                "predicate": p.get_symbolic_expr(),
                "result": p.result,
                "source_file": p.source_file,
                "source_line": p.source_line,
                "branch_id": p.branch_id,
                "semantic_tags": self._extract_semantic_tags(p)
            } for p in branch_trace]
        }
        
        with open(os.path.join(self.output_dir, "branch_trace.json"), "w") as f:
            json.dump(trace_data, f, indent=2, default=str)
    
    def export_semantic_tags(self, path):
        """Export semantic tags to JSON"""
        current_path = path.get_current_path()
        
        tags_data = {
            "timestamp": time.time(),
            "total_tags": sum(len(self._extract_semantic_tags(p)) for p in current_path),
            "per_branch_tags": [{
                "branch_index": i,
                "predicate": p.get_symbolic_expr(),
                "tags": self._extract_semantic_tags(p)
            } for i, p in enumerate(current_path)]
        }
        
        with open(os.path.join(self.output_dir, "semantic_tags.json"), "w") as f:
            json.dump(tags_data, f, indent=2, default=str)
    
    def export_all_executions(self, symbolic_inputs_list, return_values, branch_traces_list):
        """Export all executions to separate files
        
        Args:
            symbolic_inputs_list: 每次执行的 symbolic_inputs 列表
            return_values: 每次执行的返回值列表
            branch_traces_list: 每次执行的分支跟踪列表
        """
        executions_dir = os.path.join(self.output_dir, "executions")
        os.makedirs(executions_dir, exist_ok=True)
        
        for i, (symbolic_inputs, return_value, branch_trace) in enumerate(zip(
                symbolic_inputs_list, return_values, branch_traces_list)):
            
            execution_dir = os.path.join(executions_dir, f"execution_{i}")
            os.makedirs(execution_dir, exist_ok=True)
            
            # 创建临时的 JSONExporter 实例用于导出当前执行
            execution_exporter = JSONExporter(execution_dir)
            
            # 规范化路径约束
            normalizer = ConstraintNormalizer()
            raw_predicates, normalized_predicates = normalizer.normalize_path(branch_trace)
            
            # Extract semantic information
            semantic_info = {
                "path_length": len(branch_trace),
                "branch_directions": [p.result for p in branch_trace],
                "semantic_tags": [self._extract_semantic_tags(p) for p in branch_trace],
                "symbolic_variables": list(set(var for p in branch_trace for var in p.getVars())),
                "source_locations": [(p.source_file, p.source_line, p.branch_id) for p in branch_trace if p.source_file and p.source_line]
            }
            
            # 构建标准化的特征输出
            standardized_features = {
                "normalized_pc": normalized_predicates,  # 归一化的路径条件
                "branch_trace": [p.to_dict() for p in branch_trace],  # 分支跟踪
                "semantic_tags": [self._extract_semantic_tags(p) for p in branch_trace],  # 语义标签
                "source_spans": [(p.source_file, p.source_line, getattr(p, 'source_col', 0), p.branch_id) for p in branch_trace if p.source_file and p.source_line],  # 源码位置
                "path_summary": {
                    "path_length": len(branch_trace),
                    "num_variables": len(set(var for p in branch_trace for var in p.getVars())),
                    "num_branches": len([p for p in branch_trace if p.result]),
                    "num_negations": len([p for p in branch_trace if not p.result])
                },  # 路径摘要
                "exception_profile": {
                    "has_exceptions": False,  # 暂时设为 False，后续可以根据实际情况修改
                    "exception_types": []
                }  # 异常概况
            }
            
            path_data = {
                "execution_id": i,
                "timestamp": time.time(),
                "input_model": {k: v.toString() if hasattr(v, 'toString') else str(v) for k, v in symbolic_inputs.items()},
                "concrete_inputs": {k: self._get_concrete_value(v) for k, v in symbolic_inputs.items()},
                "return_value": return_value,
                "branch_trace": standardized_features["branch_trace"],
                "path_predicates_raw": [p.get_symbolic_expr() for p in branch_trace],
                "path_predicates_normalized": normalized_predicates,
                "semantic_info": semantic_info,
                "path_constraints": {
                    "assertions": [p.get_symbolic_expr() for p in branch_trace if p.result],
                    "negations": [p.get_symbolic_expr() for p in branch_trace if not p.result]
                },
                "standardized_features": standardized_features  # 添加标准化特征输出
            }
            
            with open(os.path.join(execution_dir, "path.json"), "w") as f:
                json.dump(path_data, f, indent=2, default=str)
            
            # Export branch trace for this execution
            trace_data = {
                "timestamp": time.time(),
                "trace_length": len(branch_trace),
                "branches": [{
                    "predicate": p.get_symbolic_expr(),
                    "result": p.result,
                    "source_file": p.source_file,
                    "source_line": p.source_line,
                    "branch_id": p.branch_id,
                    "semantic_tags": self._extract_semantic_tags(p)
                } for p in branch_trace]
            }
            
            with open(os.path.join(execution_dir, "branch_trace.json"), "w") as f:
                json.dump(trace_data, f, indent=2, default=str)
            
            # Export semantic tags for this execution
            tags_data = {
                "timestamp": time.time(),
                "total_tags": sum(len(self._extract_semantic_tags(p)) for p in branch_trace),
                "per_branch_tags": [{
                    "branch_index": j,
                    "predicate": p.get_symbolic_expr(),
                    "tags": self._extract_semantic_tags(p)
                } for j, p in enumerate(branch_trace)]
            }
            
            with open(os.path.join(execution_dir, "semantic_tags.json"), "w") as f:
                json.dump(tags_data, f, indent=2, default=str)
