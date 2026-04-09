# Copyright: see copyright.txt
"""
SMTLIB2 exporter for symbolic execution constraints.

Week 2: SMT export implementation
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class SMTExporter:
    """
    Exports symbolic execution constraints to SMTLIB2 format.
    """
    
    def __init__(self, output_dir: Path):
        """
        Initialize SMT exporter.
        
        Args:
            output_dir: Directory to save SMT files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_path_constraint_smt2(self,
                                   constraint,
                                   iteration_id: int = 0,
                                   solver_logic: str = "QF_BV") -> Path:
        """
        Export path constraint to SMTLIB2 format.
        
        Args:
            constraint: Path constraint object
            iteration_id: Iteration identifier
            solver_logic: SMT solver logic to use (default: QF_BV for quantifier-free bitvectors)
        
        Returns:
            Path to saved SMT2 file
        """
        # Extract predicates and convert to SMT assertions
        predicates = []
        if hasattr(constraint, 'get_path_predicates'):
            predicates = constraint.get_path_predicates()
        
        # Generate SMTLIB2 content
        smt_content = self._generate_smt2_content(predicates, solver_logic, "path")
        
        # Save to file
        filename = f"path_{iteration_id}.smt2"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(smt_content)
        
        return filepath
    
    def export_frontier_constraint_smt2(self,
                                       frontier_constraint,
                                       parent_constraint,
                                       iteration_id: int = 0,
                                       frontier_index: int = 0,
                                       solver_logic: str = "QF_BV") -> Path:
        """
        Export frontier constraint to SMTLIB2 format.
        
        Args:
            frontier_constraint: Frontier constraint object
            parent_constraint: Parent constraint
            iteration_id: Iteration identifier
            frontier_index: Index of this frontier
            solver_logic: SMT solver logic
        
        Returns:
            Path to saved SMT2 file
        """
        # Extract frontier predicates
        frontier_predicates = []
        if hasattr(frontier_constraint, 'get_path_predicates'):
            frontier_predicates = frontier_constraint.get_path_predicates()
        
        # Generate SMTLIB2 content for frontier
        smt_content = self._generate_smt2_content(frontier_predicates, solver_logic, "frontier")
        
        # Save to file
        filename = f"frontier_{iteration_id}_{frontier_index}.smt2"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(smt_content)
        
        return filepath
    
    def export_query_to_smt2(self,
                            asserts: List[str],
                            query: str,
                            negate_query: bool = True,
                            solver_logic: str = "QF_BV",
                            filename: Optional[str] = None) -> Path:
        """
        Export Z3 query to SMTLIB2 format.
        
        Args:
            asserts: List of assertion strings
            query: Query string
            negate_query: Whether to negate the query (for finding counterexamples)
            solver_logic: SMT solver logic
            filename: Optional filename (generated if not provided)
        
        Returns:
            Path to saved SMT2 file
        """
        # Generate SMTLIB2 content for query
        smt_content = self._generate_query_smt2_content(asserts, query, negate_query, solver_logic)
        
        # Determine filename
        if filename is None:
            import time
            timestamp = int(time.time())
            filename = f"query_{timestamp}.smt2"
        
        # Save to file
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(smt_content)
        
        return filepath
    
    def _generate_smt2_content(self, 
                              predicates: List[Dict], 
                              solver_logic: str,
                              constraint_type: str) -> str:
        """
        Generate SMTLIB2 content from predicates.
        
        Args:
            predicates: List of predicate dictionaries
            solver_logic: SMT solver logic
            constraint_type: Type of constraint ("path" or "frontier")
        
        Returns:
            SMTLIB2 content as string
        """
        lines = []
        
        # Header
        lines.append(f"; SMTLIB2 export - {constraint_type} constraint")
        lines.append(f"; Generated by PyExZ3")
        lines.append(f"(set-logic {solver_logic})")
        lines.append("")
        
        # Extract and declare variables
        variables = self._extract_variables_from_predicates(predicates)
        for var_name in variables:
            # We assume integer variables - adjust as needed for your representation
            lines.append(f"(declare-fun {var_name} () Int)")
        lines.append("")
        
        # Convert predicates to assertions
        for i, predicate in enumerate(predicates):
            if isinstance(predicate, dict) and 'expr' in predicate:
                expr = predicate['expr']
                result = predicate.get('result', True)
                
                # Convert Python expression to SMT expression
                smt_expr = self._python_expr_to_smt(expr)
                
                # Negate if result is False
                if not result:
                    smt_expr = f"(not {smt_expr})"
                
                lines.append(f"(assert {smt_expr})")
                lines.append(f"; Predicate {i}: {expr} (result: {result})")
                lines.append("")
        
        # Check satisfiability
        lines.append("(check-sat)")
        lines.append("(get-model)")
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_query_smt2_content(self,
                                    asserts: List[str],
                                    query: str,
                                    negate_query: bool,
                                    solver_logic: str) -> str:
        """
        Generate SMTLIB2 content for a query.
        
        Args:
            asserts: List of assertion strings
            query: Query string
            negate_query: Whether to negate the query
            solver_logic: SMT solver logic
        
        Returns:
            SMTLIB2 content as string
        """
        lines = []
        
        # Header
        lines.append("; SMTLIB2 export - Z3 query")
        lines.append("; Generated by PyExZ3")
        lines.append(f"(set-logic {solver_logic})")
        lines.append("")
        
        # Variable declarations would need to be extracted from asserts/query
        # For now, we assume they're already declared in the input strings
        lines.append("; Assertions")
        for assert_str in asserts:
            lines.append(f"(assert {assert_str})")
        lines.append("")
        
        # Query (negated for counterexample finding)
        if negate_query:
            lines.append(f"; Negated query for counterexample finding")
            lines.append(f"(assert (not {query}))")
        else:
            lines.append(f"; Query")
            lines.append(f"(assert {query})")
        lines.append("")
        
        # Check satisfiability
        lines.append("(check-sat)")
        lines.append("(get-model)")
        lines.append("")
        
        return "\n".join(lines)
    
    def _extract_variables_from_predicates(self, predicates: List[Dict]) -> List[str]:
        """
        Extract variable names from predicates.
        
        Args:
            predicates: List of predicate dictionaries
        
        Returns:
            List of variable names
        """
        variables = set()
        for predicate in predicates:
            if isinstance(predicate, dict) and 'vars' in predicate:
                if isinstance(predicate['vars'], list):
                    variables.update(predicate['vars'])
                elif isinstance(predicate['vars'], str):
                    variables.add(predicate['vars'])
        return sorted(list(variables))
    
    def _python_expr_to_smt(self, python_expr: str) -> str:
        """
        Convert Python expression to SMT expression.
        
        Note: This is a simplified conversion. A complete implementation
        would need to parse the Python expression and map operators to SMT.
        
        Args:
            python_expr: Python expression string
        
        Returns:
            SMT expression string
        """
        # Simple operator mapping
        operator_map = {
            '==': '=',
            '!=': 'distinct',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            'and': 'and',
            'or': 'or',
            'not': 'not'
        }
        
        # Simple conversion - just return as-is for now
        # In a real implementation, you'd parse the expression properly
        return f"(= {python_expr} 0)"  # Placeholder


def export_path_to_smt2(output_dir: Path,
                       constraint,
                       iteration_id: int = 0) -> Path:
    """
    Convenience function to export path constraint to SMT2.
    
    Args:
        output_dir: Directory to save SMT2 file
        constraint: Path constraint object
        iteration_id: Iteration identifier
    
    Returns:
        Path to saved SMT2 file
    """
    exporter = SMTExporter(output_dir)
    return exporter.export_path_constraint_smt2(constraint, iteration_id)