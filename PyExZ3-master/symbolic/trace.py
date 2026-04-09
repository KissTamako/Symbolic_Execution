# Copyright: see copyright.txt
"""
Execution trace module for recording execution history.

Week 1: Skeleton implementation
Week 3: Will be enhanced with more detailed trace information
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class ExecutionTrace:
    """Represents a single execution trace."""
    iteration_id: int
    path_id: str
    concrete_inputs: Dict[str, Any]
    return_value: Optional[Any]
    exception: Optional[str]
    branch_trace: List[Dict[str, Any]]
    coverage_delta: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary representation."""
        result = asdict(self)
        # Handle special serialization for non-serializable objects
        for key, value in result.items():
            if hasattr(value, '__dict__'):
                result[key] = str(value)
        return result


class TraceRecorder:
    """Records execution traces across multiple iterations."""
    
    def __init__(self):
        self.traces: List[ExecutionTrace] = []
        self.current_iteration = 0
    
    def record_execution(
        self,
        concrete_inputs: Dict[str, Any],
        return_value: Optional[Any] = None,
        exception: Optional[str] = None,
        branch_trace: Optional[List[Dict[str, Any]]] = None,
        path_id: Optional[str] = None,
        coverage_delta: Optional[int] = None
    ) -> ExecutionTrace:
        """Record a single execution."""
        if branch_trace is None:
            branch_trace = []
        
        if path_id is None:
            path_id = f"path_{self.current_iteration}"
        
        trace = ExecutionTrace(
            iteration_id=self.current_iteration,
            path_id=path_id,
            concrete_inputs=concrete_inputs,
            return_value=return_value,
            exception=exception,
            branch_trace=branch_trace,
            coverage_delta=coverage_delta
        )
        
        self.traces.append(trace)
        self.current_iteration += 1
        return trace
    
    def get_trace(self, iteration_id: int) -> Optional[ExecutionTrace]:
        """Get trace by iteration ID."""
        for trace in self.traces:
            if trace.iteration_id == iteration_id:
                return trace
        return None
    
    def get_all_traces(self) -> List[ExecutionTrace]:
        """Get all recorded traces."""
        return self.traces.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert all traces to dictionary representation."""
        return {
            "total_iterations": len(self.traces),
            "traces": [trace.to_dict() for trace in self.traces]
        }
    
    def save_to_file(self, filepath: Path) -> None:
        """Save traces to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
    
    def load_from_file(self, filepath: Path) -> None:
        """Load traces from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Note: This is a simple loading implementation
        # In a full implementation, we would properly reconstruct ExecutionTrace objects
        self.traces = []
        for trace_data in data.get('traces', []):
            trace = ExecutionTrace(**trace_data)
            self.traces.append(trace)
        
        if self.traces:
            self.current_iteration = max(t.iteration_id for t in self.traces) + 1
    
    def clear(self) -> None:
        """Clear all recorded traces."""
        self.traces = []
        self.current_iteration = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get trace statistics."""
        if not self.traces:
            return {}
        
        successful = sum(1 for t in self.traces if t.exception is None)
        failed = sum(1 for t in self.traces if t.exception is not None)
        
        unique_paths = len(set(t.path_id for t in self.traces))
        avg_branches = sum(len(t.branch_trace) for t in self.traces) / len(self.traces)
        
        return {
            "total_executions": len(self.traces),
            "successful_executions": successful,
            "failed_executions": failed,
            "unique_paths": unique_paths,
            "average_branches_per_path": round(avg_branches, 2)
        }


# Singleton instance for global access
global_tracer = TraceRecorder()


def record_execution(**kwargs) -> ExecutionTrace:
    """Convenience function to record execution using global tracer."""
    return global_tracer.record_execution(**kwargs)


def get_trace_recorder() -> TraceRecorder:
    """Get the global trace recorder instance."""
    return global_tracer


def save_traces(filepath: Path) -> None:
    """Save global traces to file."""
    global_tracer.save_to_file(filepath)


def load_traces(filepath: Path) -> None:
    """Load traces from file into global tracer."""
    global_tracer.load_from_file(filepath)


def record_branch(filename: str, line: int, branch_id: int, condition) -> None:
    """
    Record branch execution for trace recording.
    
    Args:
        filename: Source filename
        line: Line number
        branch_id: Branch identifier
        condition: Branch condition value
    """
    # This is a placeholder for branch recording
    # In a full implementation, this would record to the global trace recorder
    pass
