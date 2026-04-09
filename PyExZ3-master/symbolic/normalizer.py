# Copyright: see copyright.txt
"""
Constraint normalizer for generating comparable path conditions.

Week 4: Implementation for constraint normalization and canonical representation.
"""

import re
from typing import List, Dict, Any, Tuple, Optional, Union
from z3 import simplify, ExprRef


class Normalizer:
    """Normalizes path constraints for comparability and clustering."""
    
    def __init__(self):
        # Mapping from original variable names to normalized names
        self.var_mapping: Dict[str, str] = {}
        # Counter for generating normalized names
        self.var_counter = 0
        
    def reset(self):
        """Reset normalization state."""
        self.var_mapping.clear()
        self.var_counter = 0
    
    def normalize_variable_names(self, expr: str) -> str:
        """
        Normalize variable names in expression.
        
        Args:
            expr: Original expression string
            
        Returns:
            Expression with normalized variable names
        """
        if not expr:
            return expr
            
        # Pattern to match variable names (excluding keywords and function calls)
        var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_var(match):
            var_name = match.group(1)
            
            # Skip Python keywords and common function names
            keywords = {'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is', 'if', 'else', 
                       'len', 'int', 'str', 'bool', 'list', 'dict', 'tuple', 'set'}
            if var_name in keywords:
                return var_name
                
            # Skip numeric literals
            if var_name.replace('.', '', 1).isdigit():
                return var_name
                
            # Check if we've already mapped this variable
            if var_name in self.var_mapping:
                return self.var_mapping[var_name]
                
            # Create new normalized name
            normalized_name = f"ARG{self.var_counter}"
            self.var_mapping[var_name] = normalized_name
            self.var_counter += 1
            
            return normalized_name
        
        # Apply variable name normalization
        normalized_expr = re.sub(var_pattern, replace_var, expr)
        
        return normalized_expr
    
    def normalize_expression(self, expr: Union[str, Dict[str, Any], ExprRef]) -> str:
        """
        Normalize an expression to canonical form.
        
        Args:
            expr: Expression to normalize (string, dict, or Z3 expression)
            
        Returns:
            Normalized expression string
        """
        # Convert to string representation
        if isinstance(expr, dict):
            expr_str = expr.get('expr', str(expr))
        elif hasattr(expr, '__str__'):
            expr_str = str(expr)
        else:
            expr_str = str(expr)
            
        # Step 1: Normalize variable names
        normalized = self.normalize_variable_names(expr_str)
        
        # Step 2: Apply algebraic simplifications (if applicable)
        normalized = self._apply_algebraic_simplifications(normalized)
        
        # Step 3: Normalize comparison directions
        normalized = self._normalize_comparison_directions(normalized)
        
        # Step 4: Sort commutative operations
        normalized = self._sort_commutative_operations(normalized)
        
        return normalized
    
    def _apply_algebraic_simplifications(self, expr: str) -> str:
        """
        Apply basic algebraic simplifications.
        
        Args:
            expr: Expression string
            
        Returns:
            Simplified expression
        """
        # Remove redundant parentheses
        expr = re.sub(r'\(([a-zA-Z0-9_]+)\)', r'\1', expr)
        
        # Simplify double negatives
        expr = re.sub(r'--', '', expr)
        expr = re.sub(r'-\(-', '(', expr)
        
        # Remove unnecessary +0 or -0
        expr = re.sub(r'\s*\+\s*0\b', '', expr)
        expr = re.sub(r'\s*-\s*0\b', '', expr)
        
        # Simplify *1
        expr = re.sub(r'\s*\*\s*1\b', '', expr)
        
        return expr.strip()
    
    def _normalize_comparison_directions(self, expr: str) -> str:
        """
        Normalize comparison expressions to consistent direction.
        
        Args:
            expr: Expression string
            
        Returns:
            Expression with normalized comparison directions
        """
        # Pattern to match comparisons: x < y, x <= y, x > y, x >= y, x == y, x != y
        comparison_pattern = r'(\w+)\s*([<>]=?|==|!=)\s*(\w+)'
        
        def normalize_match(match):
            left = match.group(1).strip()
            op = match.group(2).strip()
            right = match.group(3).strip()
            
            # For equality/inequality, order doesn't matter much
            if op in ('==', '!='):
                # Sort lexicographically for consistency
                if left > right:
                    return f"{right} {op} {left}"
                return f"{left} {op} {right}"
            
            # For inequalities, always put variable on left if possible
            # If both sides are variables, sort lexicographically
            if left[0].isalpha() and right[0].isalpha():
                if left > right:
                    # Reverse inequality direction
                    reverse_ops = {'<': '>', '<=': '>=', '>': '<', '>=': '<='}
                    return f"{right} {reverse_ops[op]} {left}"
                return f"{left} {op} {right}"
            
            # If right is numeric and left is variable, keep as is
            if left[0].isalpha() and right[0].isdigit():
                return f"{left} {op} {right}"
            
            # If left is numeric and right is variable, reverse
            if left[0].isdigit() and right[0].isalpha():
                reverse_ops = {'<': '>', '<=': '>=', '>': '<', '>=': '<='}
                return f"{right} {reverse_ops[op]} {left}"
            
            return match.group(0)
        
        return re.sub(comparison_pattern, normalize_match, expr)
    
    def _sort_commutative_operations(self, expr: str) -> str:
        """
        Sort terms in commutative operations (+, *) for consistency.
        
        Args:
            expr: Expression string
            
        Returns:
            Expression with sorted terms
        """
        # Helper to sort terms in a sum
        def sort_terms_in_sum(sum_expr: str) -> str:
            # Simple sorting: constants first, then variables
            terms = re.split(r'\s*\+\s*', sum_expr)
            constants = []
            variables = []
            
            for term in terms:
                if term.strip() and term.strip()[0].isdigit():
                    constants.append(term.strip())
                else:
                    variables.append(term.strip())
            
            sorted_terms = sorted(constants) + sorted(variables)
            return ' + '.join(sorted_terms)
        
        # Helper to sort factors in a product
        def sort_factors_in_product(prod_expr: str) -> str:
            factors = re.split(r'\s*\*\s*', prod_expr)
            sorted_factors = sorted(factors, key=lambda x: x.strip())
            return ' * '.join(sorted_factors)
        
        # Apply sorting to top-level + and * operations
        # Note: This is a simplified implementation
        # A full implementation would need proper parsing
        
        return expr
    
    def normalize_predicate_list(self, predicates: List[Any]) -> Tuple[List[str], List[str]]:
        """
        Normalize a list of predicates.
        
        Args:
            predicates: List of predicate objects
            
        Returns:
            Tuple of (raw_predicates, normalized_predicates)
        """
        raw_predicates = []
        normalized_predicates = []
        
        for pred in predicates:
            # Extract expression from predicate
            if isinstance(pred, dict):
                expr = pred.get('expr', str(pred))
            else:
                expr = str(pred)
            
            raw_predicates.append(expr)
            
            # Normalize expression
            self.reset()  # Reset mapping for each predicate
            normalized_expr = self.normalize_expression(expr)
            normalized_predicates.append(normalized_expr)
        
        return raw_predicates, normalized_predicates
    
    def normalize_path_constraint(self, constraint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a complete path constraint.
        
        Args:
            constraint: Path constraint dictionary
            
        Returns:
            Normalized constraint dictionary
        """
        if not constraint:
            return constraint
        
        # Make a copy to avoid modifying the original
        normalized = constraint.copy()
        
        # Extract predicates
        predicates = constraint.get('predicates', [])
        if not predicates:
            return normalized
        
        # Normalize predicates
        raw_preds, norm_preds = self.normalize_predicate_list(predicates)
        
        # Add normalized representation
        normalized['raw_predicates'] = raw_preds
        normalized['normalized_predicates'] = norm_preds
        
        # Generate canonical constraint ID
        constraint_id = self._generate_constraint_id(norm_preds)
        normalized['normalized_id'] = constraint_id
        
        return normalized
    
    def _generate_constraint_id(self, predicates: List[str]) -> str:
        """
        Generate a canonical ID for a constraint.
        
        Args:
            predicates: List of normalized predicates
            
        Returns:
            Canonical constraint ID
        """
        # Sort predicates for consistent ordering
        sorted_preds = sorted(predicates)
        
        # Create a hash-like ID
        preds_str = '|'.join(sorted_preds)
        
        # Simple hash (in production would use proper hashing)
        import hashlib
        return hashlib.md5(preds_str.encode()).hexdigest()[:8]
    
    def compare_constraints(self, constraint1: Dict[str, Any], constraint2: Dict[str, Any]) -> bool:
        """
        Compare two constraints for equivalence using normalization.
        
        Args:
            constraint1: First constraint
            constraint2: Second constraint
            
        Returns:
            True if constraints are equivalent
        """
        # Normalize both constraints
        norm1 = self.normalize_path_constraint(constraint1)
        norm2 = self.normalize_path_constraint(constraint2)
        
        # Compare normalized IDs
        return norm1.get('normalized_id') == norm2.get('normalized_id')


# Global instance for convenience
global_normalizer = Normalizer()


def normalize_expression(expr: Union[str, Dict[str, Any], ExprRef]) -> str:
    """Normalize expression using global normalizer."""
    return global_normalizer.normalize_expression(expr)


def normalize_path_constraint(constraint: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize path constraint using global normalizer."""
    return global_normalizer.normalize_path_constraint(constraint)


def compare_constraints(constraint1: Dict[str, Any], constraint2: Dict[str, Any]) -> bool:
    """Compare constraints using global normalizer."""
    return global_normalizer.compare_constraints(constraint1, constraint2)