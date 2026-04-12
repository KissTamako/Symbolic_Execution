# Copyright: see copyright.txt
"""
SMTLIB2 exporter for symbolic execution constraints.

Week 2: SMT export implementation
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Import the new SMT converter
try:
    from ..smt_converter import SMTConverter, convert_to_smt, python_expr_to_smt
except ImportError:
    # Fallback for older versions or testing
    SMTConverter = None
    convert_to_smt = None
    python_expr_to_smt = None


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
        
        # Extract and declare variables (filter out constants)
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
                constants = predicate.get('constants', {})
                expr_tree = predicate.get('expr_tree')
                
                # Convert Python expression to SMT expression with constants and tree
                smt_expr = self._python_expr_to_smt(expr, constants, expr_tree)
                
                # Negate if result is False
                if not result:
                    smt_expr = f"(not {smt_expr})"
                
                lines.append(f"(assert {smt_expr})")
                
                # Create cleaned expression for comment
                cleaned_expr = self._clean_expression_for_comment(expr, constants)
                lines.append(f"; Predicate {i}: {cleaned_expr} (result: {result})")
                
                # Add tree structure information in comment
                if expr_tree:
                    lines.append(f"; Tree: {expr_tree}")
                
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
    
    def _python_expr_to_smt(self, python_expr: str, constants: Dict[str, Any] = None, expr_tree: Optional[List] = None) -> str:
        """
        Convert Python expression to SMT expression.
        
        Uses the new SMTConverter if available, falls back to old implementation.
        
        Args:
            python_expr: Python expression string
            constants: Dictionary of constant values to substitute
            expr_tree: Optional tree structure representation
        
        Returns:
            SMT expression string
        """
        if constants is None:
            constants = {}
        
        # First, try to use the new SMTConverter if available
        if SMTConverter is not None:
            try:
                if expr_tree:
                    # Use the tree structure if available
                    return SMTConverter.get_formula_deep(expr_tree, constants)
                else:
                    # Fallback to string conversion
                    return python_expr_to_smt(python_expr, constants, expr_tree)
            except Exception as e:
                # If conversion fails, fall back to old implementation
                print(f"Warning: SMTConverter failed, falling back: {e}")
        
        # Fallback to original implementation
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
        
        # If tree structure is provided, use it for conversion
        if expr_tree and isinstance(expr_tree, list):
            return self._tree_to_smt(expr_tree, operator_map)
        
        # Fallback to string parsing if no tree structure
        # First, substitute constants in the expression
        expr = python_expr
        for const_name, const_value in constants.items():
            # Replace const#0 with the actual value
            const_pattern = f"{const_name}#"
            if const_pattern in expr:
                # Simple substitution: replace "const#0" with "0"
                # This assumes format like "const#0"
                expr = expr.replace(f"{const_name}#0", str(const_value))
        
        # Remove symbol IDs from variable names (e.g., "a#0" -> "a")
        # This is a simplified approach - in reality we need better parsing
        import re
        
        # Remove # followed by numbers from variable names
        expr = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)#\d+', r'\1', expr)
        
        # Parse the expression
        # For now, we'll do a simple pattern matching for common expressions
        # For example: "(< a#0, const#0)" -> "(< a 0)"
        
        # Check if this is a simple comparison expression
        if expr.startswith('(') and expr.endswith(')'):
            # Remove outer parentheses
            inner = expr[1:-1]
            
            # Split by comma (this is simplified)
            parts = inner.split(', ')
            if len(parts) == 2:
                # It's a binary operation
                # Extract operator
                op_match = re.match(r'([<>=!]=?|and|or|not)', parts[0])
                if op_match:
                    op = op_match.group(1)
                    left = parts[0][len(op):].strip()
                    right = parts[1].strip()
                    
                    # Map operator to SMT
                    smt_op = operator_map.get(op, op)
                    
                    return f"({smt_op} {left} {right})"
        
        # Fallback: if we can't parse it, try to clean it up
        # Remove remaining # patterns
        expr = re.sub(r'#\d+', '', expr)
        
        # For now, just return a simple equality if we can't parse it
        return f"(= {expr} 0)"  # Placeholder fallback
    
    def _tree_to_smt(self, expr_tree: List, operator_map: Dict[str, str]) -> str:
        """
        Convert expression tree to SMT expression.
        
        Args:
            expr_tree: Expression tree (e.g., ["<", "a", 0])
            operator_map: Operator mapping dictionary
        
        Returns:
            SMT expression string
        """
        if not isinstance(expr_tree, list) or len(expr_tree) == 0:
            return "(= ? 0)"  # Fallback for invalid tree
        
        # Handle raw string fallback
        if expr_tree[0] == "raw" and len(expr_tree) > 1:
            # Try to parse the raw string
            import re
            expr = expr_tree[1]
            
            # Clean up the expression
            expr = re.sub(r'#\d+', '', expr)
            return f"(= {expr} 0)"
        
        # Extract operator and operands
        op = expr_tree[0]
        operands = expr_tree[1:]
        
        # Map operator to SMT
        smt_op = operator_map.get(op, op)
        
        # Process operands
        smt_operands = []
        for operand in operands:
            if isinstance(operand, list):
                # Recursive processing for nested expressions
                smt_operands.append(self._tree_to_smt(operand, operator_map))
            elif isinstance(operand, (int, float)):
                # Numeric literal
                smt_operands.append(str(operand))
            else:
                # Variable or string literal
                smt_operands.append(str(operand))
        
        # Build SMT expression
        if len(smt_operands) == 0:
            return f"({smt_op})"  # Unary operator like "not"
        else:
            return f"({smt_op} {' '.join(smt_operands)})"
    
    def _clean_expression_for_comment(self, expr: str, constants: Dict[str, Any] = None) -> str:
        """
        Clean expression for comment display.
        
        Args:
            expr: Original expression string
            constants: Dictionary of constant values
        
        Returns:
            Cleaned expression string
        """
        if constants is None:
            constants = {}
        
        import re
        
        # First, substitute constants
        cleaned_expr = expr
        for const_name, const_value in constants.items():
            # Replace const#0 with the actual value
            const_pattern = f"{const_name}#"
            if const_pattern in cleaned_expr:
                cleaned_expr = cleaned_expr.replace(f"{const_name}#0", str(const_value))
        
        # Remove # followed by numbers from variable names
        cleaned_expr = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)#\d+', r'\1', cleaned_expr)
        
        # Remove any remaining # patterns
        cleaned_expr = re.sub(r'#\d+', '', cleaned_expr)
        
        return cleaned_expr


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