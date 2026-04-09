# Copyright: see copyright.txt
"""
JSON exporter for symbolic execution results.

Week 2: JSON export implementation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class JSONExporter:
    """
    Exports symbolic execution results to JSON format.
    """
    
    def __init__(self, output_dir: Path):
        """
        Initialize JSON exporter.
        
        Args:
            output_dir: Directory to save JSON files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_path_constraint(self, 
                              constraint, 
                              inputs: Dict[str, Any],
                              return_value: Any,
                              exception: Optional[Exception] = None,
                              iteration_id: int = 0) -> Path:
        """
        Export path constraint to JSON.
        
        Args:
            constraint: Path constraint object
            inputs: Input values used
            return_value: Return value from execution
            exception: Exception if any
            iteration_id: Iteration identifier
        
        Returns:
            Path to saved JSON file
        """
        # Extract path predicates
        path_predicates = []
        if hasattr(constraint, 'get_path_predicates'):
            path_predicates = constraint.get_path_predicates()
        elif hasattr(constraint, 'to_dict'):
            constraint_dict = constraint.to_dict()
            if 'predicates' in constraint_dict:
                path_predicates = constraint_dict['predicates']
        
        # Build JSON structure
        path_data = {
            "export_time": datetime.now().isoformat(),
            "iteration_id": iteration_id,
            "path_info": {
                "total_branches": len(path_predicates),
                "path_id": getattr(constraint, 'path_id', f"path_{iteration_id}"),
                "is_complete": getattr(constraint, 'is_complete', True)
            },
            "inputs": self._serialize_value(inputs),
            "execution_result": {
                "return_value": self._serialize_value(return_value),
                "exception": str(exception) if exception else None,
                "success": exception is None
            },
            "path_constraint": {
                "predicates": path_predicates,
                "variables": self._extract_variables(path_predicates)
            },
            "metadata": {
                "tool": "PyExZ3",
                "version": "2.0",
                "export_format": "path_constraint"
            }
        }
        
        # Save to file
        filename = f"path_{iteration_id}.json"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(path_data, f, indent=2, default=str)
        
        return filepath
    
    def export_frontier_constraint(self,
                                  frontier_constraints: List,
                                  parent_constraint,
                                  iteration_id: int = 0) -> List[Path]:
        """
        Export frontier constraints to JSON.
        
        Args:
            frontier_constraints: List of frontier constraints
            parent_constraint: Parent constraint that generated frontiers
            iteration_id: Iteration identifier
        
        Returns:
            List of paths to saved JSON files
        """
        saved_files = []
        
        for i, constraint in enumerate(frontier_constraints):
            # Extract frontier predicates
            frontier_predicates = []
            if hasattr(constraint, 'get_path_predicates'):
                frontier_predicates = constraint.get_path_predicates()
            
            # Build frontier data
            frontier_data = {
                "export_time": datetime.now().isoformat(),
                "iteration_id": iteration_id,
                "frontier_index": i,
                "parent_path_id": getattr(parent_constraint, 'path_id', f"path_{iteration_id}"),
                "frontier_constraint": {
                    "predicates": frontier_predicates,
                    "variables": self._extract_variables(frontier_predicates),
                    "flipped_branch_index": i  # Assuming one frontier per branch flip
                },
                "metadata": {
                    "tool": "PyExZ3",
                    "version": "2.0",
                    "export_format": "frontier_constraint"
                }
            }
            
            # Save to file
            filename = f"frontier_{iteration_id}_{i}.json"
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(frontier_data, f, indent=2, default=str)
            
            saved_files.append(filepath)
        
        return saved_files
    
    def export_trace_summary(self, 
                            traces: List[Any],
                            total_iterations: int,
                            coverage_info: Optional[Dict[str, Any]] = None) -> Path:
        """
        Export trace summary to JSON.
        
        Args:
            traces: List of execution traces
            total_iterations: Total number of iterations
            coverage_info: Coverage information if available
        
        Returns:
            Path to saved JSON file
        """
        # Convert traces to serializable format
        serialized_traces = []
        for trace in traces:
            if hasattr(trace, 'to_dict'):
                serialized_traces.append(trace.to_dict())
            else:
                serialized_traces.append(self._serialize_value(trace))
        
        # Build summary data
        summary_data = {
            "export_time": datetime.now().isoformat(),
            "total_iterations": total_iterations,
            "completed_iterations": len(traces),
            "traces": serialized_traces,
            "coverage": coverage_info or {},
            "statistics": {
                "unique_paths": len(set(t.get('path_id', '') for t in serialized_traces if isinstance(t, dict))),
                "successful_executions": sum(1 for t in serialized_traces 
                                           if isinstance(t, dict) and t.get('exception') is None),
                "failed_executions": sum(1 for t in serialized_traces 
                                        if isinstance(t, dict) and t.get('exception') is not None)
            },
            "metadata": {
                "tool": "PyExZ3",
                "version": "2.0",
                "export_format": "trace_summary"
            }
        }
        
        # Save to file
        filename = "trace_summary.json"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, default=str)
        
        return filepath
    
    def _serialize_value(self, value: Any) -> Any:
        """
        Serialize value for JSON output.
        
        Args:
            value: Value to serialize
        
        Returns:
            Serialized value
        """
        if hasattr(value, 'to_dict'):
            return value.to_dict()
        elif hasattr(value, 'getConcrValue'):
            return value.getConcrValue()
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, (int, float, str, bool, type(None))):
            return value
        else:
            return str(value)
    
    def _extract_variables(self, predicates: List[Dict]) -> List[str]:
        """
        Extract unique variables from predicates.
        
        Args:
            predicates: List of predicate dictionaries
        
        Returns:
            List of unique variable names
        """
        variables = set()
        for predicate in predicates:
            if isinstance(predicate, dict) and 'vars' in predicate:
                if isinstance(predicate['vars'], list):
                    variables.update(predicate['vars'])
                elif isinstance(predicate['vars'], str):
                    variables.add(predicate['vars'])
        return sorted(list(variables))


def export_single_path(output_dir: Path,
                      constraint,
                      inputs: Dict[str, Any],
                      return_value: Any,
                      exception: Optional[Exception] = None,
                      iteration_id: int = 0) -> Path:
    """
    Convenience function to export a single path constraint.
    
    Args:
        output_dir: Directory to save JSON file
        constraint: Path constraint object
        inputs: Input values used
        return_value: Return value from execution
        exception: Exception if any
        iteration_id: Iteration identifier
    
    Returns:
        Path to saved JSON file
    """
    exporter = JSONExporter(output_dir)
    return exporter.export_path_constraint(constraint, inputs, return_value, exception, iteration_id)