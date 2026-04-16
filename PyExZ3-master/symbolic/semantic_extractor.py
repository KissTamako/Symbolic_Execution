import ast
import re

class SemanticExtractor:
    def extract_semantic_tags(self, path):
        """Extract semantic tags from a path using AST analysis"""
        tags = []
        predicates = path.get_current_path()
        
        for pred in predicates:
            # Get symbolic expression
            sym_type = pred.symtype
            expr = None
            
            # Try to get the expression from different sources
            if hasattr(sym_type, 'expr') and sym_type.expr:
                expr = sym_type.expr
            
            # Extract tags based on expression structure
            if expr:
                tags.extend(self._analyze_expression(expr))
            
            # Extract tags based on predicate result
            if pred.result:
                tags.append("branch-taken")
            else:
                tags.append("branch-not-taken")
            
            # Extract tags based on source location
            if pred.source_file and pred.source_line:
                tags.append(f"location:{pred.source_file}:{pred.source_line}")
        
        return list(set(tags))  # Remove duplicates
    
    def _analyze_expression(self, expr):
        """Analyze expression structure and extract semantic tags"""
        tags = []
        
        if isinstance(expr, list) and len(expr) > 0:
            op = expr[0]
            args = expr[1:]
            
            # Analyze operation type
            if op in ['+', '-', '*', '/', '//', '%', '**']:
                tags.append(f"arithmetic:{op}")
                if op in ['/', '//']:
                    tags.append("division-operation")
            elif op in ['<', '>', '<=', '>=', '==', '!=']:
                tags.append(f"comparison:{op}")
                # Check for specific comparison patterns
                for arg in args:
                    if isinstance(arg, (int, float)):
                        if arg < 0:
                            tags.append("negative-check")
                        elif arg == 0:
                            tags.append("zero-check")
            elif op in ['and', 'or', 'not']:
                tags.append(f"logical:{op}")
            elif op == 'abs':
                tags.append("absolute-value")
            elif op == 'len':
                tags.append("length-operation")
            elif op == 'in':
                tags.append("contains-check")
            elif op == 'startswith':
                tags.append("prefix-check")
            elif op == 'endswith':
                tags.append("suffix-check")
            elif op == 'getitem':
                tags.append("index-operation")
                tags.append("index-out-of-range-risk")
            
            # Recursively analyze arguments
            for arg in args:
                tags.extend(self._analyze_expression(arg))
        elif isinstance(expr, str):
            # String literal analysis
            if expr == '':
                tags.append("empty-string")
            tags.append("string-literal")
        elif isinstance(expr, (int, float)):
            # Numeric literal analysis
            if expr < 0:
                tags.append("negative-literal")
            elif expr == 0:
                tags.append("zero-literal")
            elif expr == 1:
                tags.append("one-literal")
            tags.append("numeric-literal")
        
        return tags
    
    def generate_execution_summary(self, path, return_value, exception):
        """Generate execution summary with enhanced semantic information"""
        predicates = path.get_current_path()
        
        # Extract semantic tags for the entire path
        path_tags = self.extract_semantic_tags(path)
        
        # Analyze predicate types
        predicate_types = []
        for pred in predicates:
            sym_type = pred.symtype
            if hasattr(sym_type, '__class__'):
                predicate_types.append(sym_type.__class__.__name__)
        
        summary = {
            "key_judgments": [p.toString() for p in predicates],
            "return_value": return_value,
            "exception": str(exception) if exception else None,
            "source_locations": [(p.source_file, p.source_line) for p in predicates if p.source_file and p.source_line],
            "semantic_tags": path_tags,
            "predicate_types": list(set(predicate_types)),
            "path_length": len(predicates),
            "branch_statistics": {
                "taken": sum(1 for p in predicates if p.result),
                "not_taken": sum(1 for p in predicates if not p.result)
            }
        }
        return summary
