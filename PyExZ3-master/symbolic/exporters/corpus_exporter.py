# Copyright: see copyright.txt
"""
Corpus exporter for generating clustering-ready data from symbolic execution.

Week 4: Implementation for corpus generation in JSONL format.
References PyCT-master's statistics collection approach and integrates with
PyExZ3's existing export infrastructure.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, TYPE_CHECKING
from datetime import datetime

# ========= 1. 类型检查专用 =========
if TYPE_CHECKING:
    from .json_exporter import JSONExporter as _JSONExporter_Type
    from ..semantic_extractor import SemanticExtractor
    from ..trace import TraceRecorder

# ========= 2. 运行时导入 =========
try:
    from .json_exporter import JSONExporter as _JSONExporter_Runtime
    from ..normalizer import normalize_path_constraint as _normalize_path_constraint
    from ..semantic_extractor import SemanticExtractor as _SemanticExtractor_Runtime
    from ..trace import TraceRecorder as _TraceRecorder_Runtime
except ImportError:
    _JSONExporter_Runtime = None
    _SemanticExtractor_Runtime = None
    _TraceRecorder_Runtime = None
    def _normalize_path_constraint(constraint):
        return constraint

# ========= 3. 运行时绑定 =========
JSONExporter = _JSONExporter_Runtime
SemanticExtractor = _SemanticExtractor_Runtime
TraceRecorder = _TraceRecorder_Runtime
normalize_path_constraint = _normalize_path_constraint


class CorpusExporter:
    """
    Exports symbolic execution results to corpus format for clustering.
    
    Generates corpus.jsonl (JSON Lines) with each line containing a complete
    path record suitable for PaCon-style clustering experiments.
    """
    
    def __init__(self, output_dir: Path):
        """
        Initialize corpus exporter.
        
        Args:
            output_dir: Directory to save corpus files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize semantic extractor if available
        self.semantic_extractor = None
        if SemanticExtractor is not None:
            try:
                self.semantic_extractor = SemanticExtractor()
            except:
                pass
        
        # Track program and submission IDs
        self.program_id = None
        self.submission_id = None
        
    def set_program_info(self, program_id: str, submission_id: Optional[str] = None):
        """
        Set program and submission identifiers for corpus records.
        
        Args:
            program_id: Identifier for the program being analyzed
            submission_id: Optional submission identifier (for multiple submissions)
        """
        self.program_id = program_id
        self.submission_id = submission_id or f"{program_id}_submission"
    
    def export_corpus_record(self,
                           path_data: Dict[str, Any],
                           iteration_id: int = 0,
                           coverage_info: Optional[Dict[str, Any]] = None,
                           additional_metadata: Optional[Dict[str, Any]] = None) -> Path:
        """
        Export a single path execution to corpus format.
        
        Args:
            path_data: Path data from JSON exporter or similar
            iteration_id: Iteration identifier
            coverage_info: Coverage information if available
            additional_metadata: Additional metadata to include
            
        Returns:
            Path to corpus.jsonl file (appends to existing file)
        """
        # Generate corpus record
        corpus_record = self._build_corpus_record(
            path_data, iteration_id, coverage_info, additional_metadata
        )
        
        # Append to corpus.jsonl file
        corpus_file = self.output_dir / "corpus.jsonl"
        with open(corpus_file, 'a', encoding='utf-8') as f:
            json.dump(corpus_record, f, ensure_ascii=False, default=str)
            f.write('\n')
        
        return corpus_file
    
    def export_batch(self,
                    path_records: List[Dict[str, Any]],
                    coverage_info: Optional[Dict[str, Any]] = None) -> Path:
        """
        Export multiple path records to corpus format.
        
        Args:
            path_records: List of path data dictionaries
            coverage_info: Coverage information if available
            
        Returns:
            Path to corpus.jsonl file
        """
        corpus_records = []
        
        for i, path_data in enumerate(path_records):
            record = self._build_corpus_record(
                path_data, i, coverage_info
            )
            corpus_records.append(record)
        
        # Write all records to corpus.jsonl
        corpus_file = self.output_dir / "corpus.jsonl"
        with open(corpus_file, 'w', encoding='utf-8') as f:
            for record in corpus_records:
                json.dump(record, f, ensure_ascii=False, default=str)
                f.write('\n')
        
        return corpus_file
    
    def _build_corpus_record(self,
                           path_data: Dict[str, Any],
                           iteration_id: int,
                           coverage_info: Optional[Dict[str, Any]] = None,
                           additional_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build a corpus record from path data.
        
        Args:
            path_data: Path data dictionary
            iteration_id: Iteration identifier
            coverage_info: Coverage information
            additional_metadata: Additional metadata
            
        Returns:
            Corpus record dictionary
        """
        # Extract basic information from path_data
        path_id = path_data.get('path_info', {}).get('path_id', f"path_{iteration_id}")
        inputs = path_data.get('inputs', [])
        execution_result = path_data.get('execution_result', {})
        path_constraint = path_data.get('path_constraint', {})
        normalized_constraint = path_data.get('normalized_constraint', {})
        
        # Extract predicates
        predicates = path_constraint.get('predicates', [])
        
        # Extract raw and normalized predicates
        raw_predicates = normalized_constraint.get('raw_predicates', [])
        if not raw_predicates and predicates:
            # Fallback: extract expressions from predicates
            raw_predicates = [p.get('expr', str(p)) for p in predicates]
        
        normalized_predicates = normalized_constraint.get('normalized_predicates', [])
        
        # Extract branch trace
        branch_trace = self._extract_branch_trace(predicates)
        
        # Extract semantic tags
        semantic_tags = self._extract_semantic_tags(predicates, execution_result)
        
        # Determine outcome
        outcome = self._determine_outcome(execution_result)
        
        # Calculate coverage delta (simplified - could be enhanced)
        coverage_delta = self._calculate_coverage_delta(coverage_info, iteration_id)
        
        # Build corpus record
        corpus_record = {
            # Identifiers (Week 4 requirement)
            "program_id": self.program_id or "unknown_program",
            "submission_id": self.submission_id or "unknown_submission",
            "path_id": path_id,
            
            # Execution data
            "iteration_id": iteration_id,
            "export_time": datetime.now().isoformat(),
            
            # Inputs and constraints (Week 4 requirement)
            "inputs": inputs,
            "raw_pc": raw_predicates,
            "normalized_pc": normalized_predicates,
            
            # Branch and semantic information (Week 4 requirement)
            "branch_trace": branch_trace,
            "semantic_tags": semantic_tags,
            
            # Outcome and coverage (Week 4 requirement)
            "outcome": outcome,
            "coverage_delta": coverage_delta,
            
            # Additional execution details
            "execution_result": {
                "return_value": execution_result.get('return_value'),
                "exception": execution_result.get('exception'),
                "success": execution_result.get('success', False)
            },
            
            # Constraint information
            "constraint_info": {
                "predicate_count": len(predicates),
                "variables": path_constraint.get('variables', []),
                "normalized_id": normalized_constraint.get('normalized_id')
            },
            
            # Metadata
            "metadata": {
                "tool": "PyExZ3",
                "version": "2.0",
                "export_format": "corpus_record",
                "week": 4
            }
        }
        
        # Add additional metadata if provided
        if additional_metadata:
            corpus_record["additional_metadata"] = additional_metadata
        
        # Add coverage info if available
        if coverage_info:
            corpus_record["coverage_info"] = coverage_info
        
        return corpus_record
    
    def _extract_branch_trace(self, predicates: List[Dict]) -> List[Dict]:
        """
        Extract branch trace information from predicates.
        
        Args:
            predicates: List of predicate dictionaries
            
        Returns:
            List of branch trace entries
        """
        branch_trace = []
        
        for i, pred in enumerate(predicates):
            if isinstance(pred, dict):
                branch_entry = {
                    "branch_index": i,
                    "expr": pred.get('expr', ''),
                    "result": pred.get('result'),
                    "source_file": pred.get('source_file'),
                    "source_line": pred.get('source_line'),
                    "branch_id": pred.get('branch_id'),
                    "variables": pred.get('vars', [])
                }
                branch_trace.append(branch_entry)
        
        return branch_trace
    
    def _extract_semantic_tags(self, 
                             predicates: List[Dict], 
                             execution_result: Dict[str, Any]) -> List[str]:
        """
        Extract semantic tags from predicates and execution result.
        
        Args:
            predicates: List of predicate dictionaries
            execution_result: Execution result dictionary
            
        Returns:
            List of semantic tags
        """
        tags = []
        
        # Use semantic extractor if available
        if self.semantic_extractor:
            try:
                # Extract tags from predicates
                for pred in predicates:
                    if isinstance(pred, dict):
                        expr = pred.get('expr', '')
                        if expr:
                            extracted = self.semantic_extractor.extract_tags_from_expr(expr)
                            tags.extend(extracted)
            except:
                pass
        
        # Add exception-related tags
        exception = execution_result.get('exception')
        if exception:
            if "ZeroDivisionError" in str(exception):
                tags.append("division-by-zero-risk")
            elif "IndexError" in str(exception) or "out of range" in str(exception).lower():
                tags.append("index-out-of-range-risk")
            elif "ValueError" in str(exception):
                tags.append("value-error-path")
            tags.append("exception-path")
        
        # Add basic rule-based tags
        for pred in predicates:
            if isinstance(pred, dict):
                expr = pred.get('expr', '').lower()
                result = pred.get('result')
                
                # Check for zero-related conditions
                if '== 0' in expr or '==0' in expr:
                    tags.append("zero-check")
                elif '!= 0' in expr or '!=0' in expr:
                    tags.append("non-zero-check")
                
                # Check for negative conditions
                if '< 0' in expr or '<0' in expr:
                    tags.append("negative-check")
                
                # Check for length conditions
                if 'len(' in expr:
                    tags.append("length-bound-check")
        
        # Remove duplicates and return
        return list(set(tags))
    
    def _determine_outcome(self, execution_result: Dict[str, Any]) -> str:
        """
        Determine the outcome of execution.
        
        Args:
            execution_result: Execution result dictionary
            
        Returns:
            Outcome string: "success", "exception", "timeout", etc.
        """
        success = execution_result.get('success', False)
        exception = execution_result.get('exception')
        
        if success:
            return "success"
        elif exception:
            if "Timeout" in str(exception):
                return "timeout"
            else:
                return "exception"
        else:
            return "unknown"
    
    def _calculate_coverage_delta(self, 
                                coverage_info: Optional[Dict[str, Any]], 
                                iteration_id: int) -> float:
        """
        Calculate coverage delta for this iteration.
        
        Args:
            coverage_info: Coverage information dictionary
            iteration_id: Current iteration ID
            
        Returns:
            Coverage delta value (0.0-1.0)
        """
        if not coverage_info:
            return 0.0
        
        # Simplified implementation - in reality would track coverage changes
        # This is a placeholder that could be enhanced with actual coverage tracking
        try:
            # Try to extract coverage information
            total_lines = coverage_info.get('total_lines', 100)
            covered_lines = coverage_info.get('covered_lines', 0)
            
            if total_lines > 0:
                return covered_lines / total_lines
        except:
            pass
        
        # Fallback: use iteration-based pseudo-coverage
        return min(1.0, iteration_id * 0.1)
    
    def export_from_json_exporter(self,
                                 json_exporter: "_JSONExporter_Type",
                                 constraint,
                                 inputs: Dict[str, Any],
                                 return_value: Any,
                                 exception: Optional[Exception] = None,
                                 iteration_id: int = 0,
                                 coverage_info: Optional[Dict[str, Any]] = None) -> Path:
        """
        Convenience method to export corpus record directly from execution data.
        
        Args:
            json_exporter: JSONExporter instance
            constraint: Path constraint object
            inputs: Input values used
            return_value: Return value from execution
            exception: Exception if any
            iteration_id: Iteration identifier
            coverage_info: Coverage information
            
        Returns:
            Path to corpus.jsonl file
        """
        # First export to JSON to get structured data
        json_file = json_exporter.export_path_constraint(
            constraint, inputs, return_value, exception, iteration_id
        )
        
        # Read the JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            path_data = json.load(f)
        
        # Export to corpus format
        return self.export_corpus_record(
            path_data, iteration_id, coverage_info
        )


def export_corpus_batch(output_dir: Union[str, Path],
                       path_records: List[Dict[str, Any]],
                       program_id: str,
                       submission_id: Optional[str] = None,
                       coverage_info: Optional[Dict[str, Any]] = None) -> Path:
    """
    Convenience function to export a batch of path records to corpus format.
    
    Args:
        output_dir: Directory to save corpus file
        path_records: List of path data dictionaries
        program_id: Program identifier
        submission_id: Submission identifier
        coverage_info: Coverage information
        
    Returns:
        Path to corpus.jsonl file
    """
    output_dir = Path(output_dir)
    exporter = CorpusExporter(output_dir)
    exporter.set_program_info(program_id, submission_id)
    
    return exporter.export_batch(path_records, coverage_info)


def export_single_to_corpus(output_dir: Union[str, Path],
                          path_data: Dict[str, Any],
                          program_id: str,
                          submission_id: Optional[str] = None,
                          iteration_id: int = 0,
                          coverage_info: Optional[Dict[str, Any]] = None) -> Path:
    """
    Convenience function to export a single path record to corpus format.
    
    Args:
        output_dir: Directory to save corpus file
        path_data: Path data dictionary
        program_id: Program identifier
        submission_id: Submission identifier
        iteration_id: Iteration identifier
        coverage_info: Coverage information
        
    Returns:
        Path to corpus.jsonl file
    """
    output_dir = Path(output_dir)
    exporter = CorpusExporter(output_dir)
    exporter.set_program_info(program_id, submission_id)
    
    return exporter.export_corpus_record(
        path_data, iteration_id, coverage_info
    )