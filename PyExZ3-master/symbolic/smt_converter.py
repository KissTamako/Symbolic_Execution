# Copyright: see copyright.txt
"""
SMT conversion utilities for PyExZ3.

This module provides functions to convert Python expressions and values
to SMTLIB2 format, based on PyCT's implementation with adaptations for
PyExZ3's architecture.
"""

import re
from typing import Any, Union, List, Dict, Optional


def py2smt(x: Any) -> str:
    """
    Convert Python object to SMTLIB2 string constant.
    
    Based on PyCT's py2smt function with improvements for PyExZ3.
    
    Args:
        x: Python object to convert
        
    Returns:
        SMTLIB2 string representation
        
    Raises:
        NotImplementedError: For unsupported types
    """
    if type(x) is bool:
        return 'true' if x else 'false'
    
    if type(x) in (float, int):
        # Handle negative numbers using SMT's (- x) syntax
        if x < 0:
            return '(- ' + str(-x) + ')'
        return str(x)
    
    if type(x) is str:
        # Escape special characters
        x = x.replace("\\", "\\\\")  # Backslash
        x = x.replace("\r", "\\r")   # Carriage return
        x = x.replace("\n", "\\n")   # Newline
        x = x.replace("\t", "\\t")   # Tab
        x = x.replace('"', '""')     # Double quote
        
        # Handle Unicode characters
        x_new = ""
        for ch in x:
            if ord(ch) > 127:  # Unicode characters
                # Format: \u{hex} (SMTLIB2 Unicode escape)
                x_new += '\\u{' + str(hex(ord(ch)))[2:] + '}'
            else:
                x_new += ch
        
        # All string constants must be enclosed by double quotes in SMTLIB2
        return '"' + x_new + '"'
    
    # Try to handle other numeric types
    if hasattr(x, '__float__'):
        try:
            value = float(x)
            if value < 0:
                return '(- ' + str(-value) + ')'
            return str(value)
        except (ValueError, TypeError):
            pass
    
    raise NotImplementedError(f"Unsupported type for py2smt: {type(x)}")


class SMTConverter:
    """
    Converts expression trees to SMTLIB2 format.
    
    This class provides methods for converting PyExZ3's expression trees
    to SMTLIB2 format, supporting both deep (symbolic) and shallow
    (concrete) conversions.
    """
    
    # Operator mapping from Python to SMTLIB2
    OPERATOR_MAP = {
        # Arithmetic operators
        '+': '+',
        '-': '-',
        '*': '*',
        '/': 'div',  # Integer division
        '%': 'mod',
        
        # Comparison operators
        '==': '=',
        '!=': 'distinct',
        '<': '<',
        '<=': '<=',
        '>': '>',
        '>=': '>=',
        
        # Logical operators
        'and': 'and',
        'or': 'or',
        'not': 'not',
        
        # Bitwise operators (if supported)
        '&': 'bvand',
        '|': 'bvor',
        '^': 'bvxor',
        '~': 'bvnot',
        '<<': 'bvshl',
        '>>': 'bvlshr',
    }
    
    @classmethod
    def get_formula_deep(cls, expr_tree: Any, constants: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert expression tree to SMT formula in deep mode (full symbolic).
        
        Args:
            expr_tree: Expression tree or value
            constants: Optional dictionary of constant values
            
        Returns:
            SMTLIB2 formula string
        """
        return cls._get_formula(expr_tree, deep=True, constants=constants)
    
    @classmethod
    def get_formula_shallow(cls, expr_tree: Any, constants: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert expression tree to SMT formula in shallow mode (concrete values).
        
        Args:
            expr_tree: Expression tree or value
            constants: Optional dictionary of constant values
            
        Returns:
            SMTLIB2 formula string
        """
        return cls._get_formula(expr_tree, deep=False, constants=constants)
    
    @classmethod
    def _get_formula(cls, expr: Any, deep: bool, constants: Optional[Dict[str, Any]] = None) -> str:
        """
        Internal method for converting expressions to SMT.
        
        Args:
            expr: Expression to convert
            deep: Whether to convert in deep mode
            constants: Dictionary of constant values
            
        Returns:
            SMTLIB2 formula string
        """
        if constants is None:
            constants = {}
        
        # Handle raw string fallback
        if isinstance(expr, list) and len(expr) > 0 and expr[0] == "raw":
            # This is a raw string expression that couldn't be parsed
            if len(expr) > 1:
                # Try to clean it up
                import re
                cleaned = re.sub(r'#\d+', '', expr[1])
                # Try to extract operator and operands
                if cleaned.startswith('(') and cleaned.endswith(')'):
                    inner = cleaned[1:-1]
                    parts = inner.split(', ')
                    if len(parts) == 2:
                        # Try to parse as binary operation
                        op_match = re.match(r'([<>=!]=?|and|or|not)', parts[0])
                        if op_match:
                            op = op_match.group(1)
                            left = parts[0][len(op):].strip()
                            right = parts[1].strip()
                            
                            # Clean variable names
                            left = re.sub(r'#\d+', '', left)
                            right = re.sub(r'#\d+', '', right)
                            
                            # Handle constants
                            if left in constants:
                                left = constants[left]
                            if right in constants:
                                right = constants[right]
                            
                            smt_op = cls.OPERATOR_MAP.get(op, op)
                            return f"({smt_op} {left} {right})"
                return f"(= {cleaned} 0)"  # Fallback
        
        # Handle list expressions (tree structure)
        if isinstance(expr, list) and len(expr) > 0:
            op = expr[0]
            operands = expr[1:]
            
            # Map operator to SMT
            smt_op = cls.OPERATOR_MAP.get(op, op)
            
            # Process operands
            smt_operands = []
            for operand in operands:
                if isinstance(operand, list):
                    # Recursive processing for nested expressions
                    smt_operands.append(cls._get_formula(operand, deep, constants))
                elif deep:
                    # In deep mode, preserve symbolic variables
                    if isinstance(operand, str) and operand in constants:
                        # This is a constant variable name
                        smt_operands.append(py2smt(constants[operand]))
                    else:
                        smt_operands.append(str(operand))
                else:
                    # In shallow mode, use concrete values
                    if isinstance(operand, str) and operand in constants:
                        smt_operands.append(py2smt(constants[operand]))
                    else:
                        try:
                            # Try to convert to SMT constant
                            smt_operands.append(py2smt(operand))
                        except NotImplementedError:
                            # Fallback to string representation
                            smt_operands.append(str(operand))
            
            # Build SMT expression
            if len(smt_operands) == 0:
                return f"({smt_op})"  # Unary operator like "not"
            else:
                return f"({smt_op} {' '.join(smt_operands)})"
        
        # Handle simple values
        if deep:
            # In deep mode, preserve variables as strings
            if isinstance(expr, str) and expr in constants:
                return py2smt(constants[expr])
            return str(expr)
        else:
            # In shallow mode, convert to SMT constant
            if isinstance(expr, str) and expr in constants:
                return py2smt(constants[expr])
            try:
                return py2smt(expr)
            except NotImplementedError:
                return str(expr)
    
    @classmethod
    def extract_variables(cls, expr_tree: Any, constants: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Extract variable names from expression tree.
        
        Args:
            expr_tree: Expression tree to analyze
            constants: Optional dictionary of constant values to exclude
            
        Returns:
            List of variable names
        """
        if constants is None:
            constants = {}
        
        variables = set()
        
        def _traverse(expr):
            if isinstance(expr, list):
                # Recursively traverse list expressions
                for item in expr:
                    _traverse(item)
            elif isinstance(expr, str):
                # Check if it's a variable (not a constant and not an operator)
                if expr not in constants and expr not in cls.OPERATOR_MAP:
                    # Basic variable name validation
                    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
                        variables.add(expr)
        
        _traverse(expr_tree)
        return sorted(list(variables))
    
    @classmethod
    def generate_variable_declarations(cls, variables: List[str], var_types: Optional[Dict[str, str]] = None) -> List[str]:
        """
        Generate SMTLIB2 variable declarations.
        
        Args:
            variables: List of variable names
            var_types: Optional dictionary mapping variable names to types
            
        Returns:
            List of SMTLIB2 declare-fun statements
        """
        declarations = []
        default_type = "Int"  # Default type for variables
        
        for var in variables:
            var_type = default_type
            if var_types and var in var_types:
                var_type = var_types[var]
            
            declarations.append(f"(declare-fun {var} () {var_type})")
        
        return declarations
    
    @classmethod
    def clean_expression_string(cls, expr_str: str, constants: Optional[Dict[str, Any]] = None) -> str:
        """
        Clean expression string for display in comments.
        
        Args:
            expr_str: Original expression string
            constants: Optional dictionary of constant values
            
        Returns:
            Cleaned expression string
        """
        if constants is None:
            constants = {}
        
        # First, substitute constants
        cleaned = expr_str
        for const_name, const_value in constants.items():
            # Replace const#0 with actual value
            const_pattern = f"{const_name}#"
            if const_pattern in cleaned:
                cleaned = cleaned.replace(f"{const_name}#0", str(const_value))
        
        # Remove # followed by numbers from variable names
        cleaned = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)#\d+', r'\1', cleaned)
        
        # Remove any remaining # patterns
        cleaned = re.sub(r'#\d+', '', cleaned)
        
        return cleaned


# Convenience functions
def convert_to_smt(expr: Any, deep: bool = True, constants: Optional[Dict[str, Any]] = None) -> str:
    """
    Convert expression to SMTLIB2 format.
    
    Args:
        expr: Expression to convert
        deep: Whether to convert in deep mode
        constants: Optional dictionary of constant values
        
    Returns:
        SMTLIB2 formula string
    """
    if deep:
        return SMTConverter.get_formula_deep(expr, constants)
    else:
        return SMTConverter.get_formula_shallow(expr, constants)


def python_expr_to_smt(expr_str: str, constants: Optional[Dict[str, Any]] = None, expr_tree: Optional[List] = None) -> str:
    """
    Convert Python expression string to SMT expression.
    
    This function provides backward compatibility with the old interface.
    
    Args:
        expr_str: Python expression string
        constants: Optional dictionary of constant values
        expr_tree: Optional expression tree
        
    Returns:
        SMT expression string
    """
    if expr_tree:
        # Use the tree structure if available
        return SMTConverter.get_formula_deep(expr_tree, constants)
    
    # Fallback to string parsing
    # This maintains compatibility with old code
    if constants is None:
        constants = {}
    
    # Import here to avoid circular imports
    import re
    
    # First, substitute constants
    expr = expr_str
    for const_name, const_value in constants.items():
        # Replace const#0 with the actual value
        const_pattern = f"{const_name}#"
        if const_pattern in expr:
            expr = expr.replace(f"{const_name}#0", str(const_value))
    
    # Remove symbol IDs from variable names
    expr = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)#\d+', r'\1', expr)
    
    # Check if this is a simple comparison expression
    if expr.startswith('(') and expr.endswith(')'):
        # Remove outer parentheses
        inner = expr[1:-1]
        
        # Split by comma
        parts = inner.split(', ')
        if len(parts) == 2:
            # Extract operator
            op_match = re.match(r'([<>=!]=?|and|or|not)', parts[0])
            if op_match:
                op = op_match.group(1)
                left = parts[0][len(op):].strip()
                right = parts[1].strip()
                
                # Map operator to SMT
                smt_op = SMTConverter.OPERATOR_MAP.get(op, op)
                
                return f"({smt_op} {left} {right})"
    
    # Fallback
    expr = re.sub(r'#\d+', '', expr)
    return f"(= {expr} 0)"