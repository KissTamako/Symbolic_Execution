# Copyright: see copyright.txt
"""
Semantic tag extractor for analyzing path constraints.

Week 1: Skeleton implementation
Week 3: Will implement actual semantic analysis
"""

import re
from typing import List, Set, Dict, Any, Optional


class SemanticExtractor:
    """Extracts semantic tags from path constraints and execution traces."""
    
    def __init__(self):
        # Tag patterns for rule-based extraction
        self.tag_patterns = {
            'negative-check': [
                r'<\s*0',
                r'<=\s*-1',
                r'negative',
                r'<\s*zero',
                r'-\d+'
            ],
            'zero-check': [
                r'==\s*0',
                r'!=\s*0',
                r'zero',
                r'<\s*1'
            ],
            'empty-string-check': [
                r'len\([^)]*\)\s*==\s*0',
                r'==\s*""',
                r'empty',
                r'len\s*<\s*1'
            ],
            'length-bound-check': [
                r'len\([^)]*\)',
                r'length',
                r'size\(\)',
                r'\.length'
            ],
            'contains-check': [
                r'in\s+',
                r'contains\(',
                r'find\([^)]*\)\s*!=\s*-1',
                r'index\([^)]*\)\s*>=\s*0'
            ],
            'prefix-check': [
                r'startswith\(',
                r'^[^=]*==\s*"[^"]*"',
                r'prefix'
            ],
            'suffix-check': [
                r'endswith\(',
                r'[^=]*==\s*"[^"]*"$',
                r'suffix'
            ],
            'division-by-zero-risk': [
                r'/\s*0',
                r'%\s*0',
                r'division.*zero',
                r'divide.*zero'
            ],
            'index-out-of-range-risk': [
                r'\[\s*\d+\s*\]',
                r'index\s*>=\s*len',
                r'index\s*>\s*\d+',
                r'out.*range'
            ],
            'exception-path': [
                r'except',
                r'try',
                r'raise',
                r'Exception'
            ]
        }
        
        # Compile patterns
        self.compiled_patterns = {}
        for tag, patterns in self.tag_patterns.items():
            compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
            self.compiled_patterns[tag] = compiled
    
    def extract_tags_from_expr(self, expr: str) -> Set[str]:
        """Extract semantic tags from a single expression string."""
        tags = set()
        
        if not expr:
            return tags
        
        expr_lower = expr.lower()
        
        # Check each tag pattern
        for tag, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(expr):
                    tags.add(tag)
                    break
        
        # Additional heuristic checks
        if 'index' in expr_lower and ('<' in expr or '>' in expr or '>=' in expr or '<=' in expr):
            tags.add('index-out-of-range-risk')
        
        if 'division' in expr_lower or '/' in expr or '%' in expr:
            if '0' in expr:
                tags.add('division-by-zero-risk')
        
        return tags
    
    def extract_tags_from_predicates(self, predicates: List[Dict[str, Any]]) -> Set[str]:
        """Extract semantic tags from a list of predicates."""
        tags = set()
        
        for pred in predicates:
            if isinstance(pred, dict):
                expr = pred.get('expr', '')
            else:
                expr = str(pred)
            
            tags.update(self.extract_tags_from_expr(expr))
        
        return tags
    
    def extract_tags_from_trace(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Extract semantic tags from an execution trace."""
        if not trace:
            return {}
        
        tags = set()
        
        # Extract from branch trace
        if 'branch_trace' in trace and trace['branch_trace']:
            for branch in trace['branch_trace']:
                if isinstance(branch, dict) and 'expr' in branch:
                    tags.update(self.extract_tags_from_expr(branch['expr']))
        
        # Check for exceptions
        if trace.get('exception'):
            tags.add('exception-path')
        
        # Check return values
        return_value = trace.get('return_value')
        if return_value is not None:
            if isinstance(return_value, (int, float)) and return_value < 0:
                tags.add('negative-check')
            elif return_value == 0:
                tags.add('zero-check')
            elif isinstance(return_value, str) and return_value == "":
                tags.add('empty-string-check')
        
        return {
            'semantic_tags': list(tags),
            'tag_count': len(tags),
            'has_exception': 'exception-path' in tags,
            'has_division_risk': 'division-by-zero-risk' in tags,
            'has_index_risk': 'index-out-of-range-risk' in tags
        }
    
    def generate_summary(self, trace: Dict[str, Any], tags: Set[str]) -> Dict[str, Any]:
        """Generate human-readable summary for a trace."""
        summary = {
            'path_id': trace.get('path_id', 'unknown'),
            'iteration_id': trace.get('iteration_id', -1),
            'key_conditions': [],
            'core_condition': None,
            'outcome': 'normal'
        }
        
        # Determine outcome
        if 'exception-path' in tags:
            summary['outcome'] = 'exception'
        elif trace.get('exception'):
            summary['outcome'] = 'exception'
        elif trace.get('return_value') is None:
            summary['outcome'] = 'no_return'
        else:
            summary['outcome'] = 'normal_return'
        
        # Extract key conditions from branch trace
        if 'branch_trace' in trace and trace['branch_trace']:
            for branch in trace['branch_trace']:
                if isinstance(branch, dict) and 'expr' in branch:
                    expr = branch['expr']
                    # Simple heuristic: conditions with variables are more interesting
                    if any(c.isalpha() for c in expr):
                        summary['key_conditions'].append({
                            'expr': expr,
                            'source_line': branch.get('source_line'),
                            'branch_id': branch.get('branch_id')
                        })
            
            # Use the last condition as core condition (simplistic approach)
            if summary['key_conditions']:
                summary['core_condition'] = summary['key_conditions'][-1]
        
        # Add semantic insights
        semantic_insights = []
        if 'division-by-zero-risk' in tags:
            semantic_insights.append("Path contains division by zero risk")
        if 'index-out-of-range-risk' in tags:
            semantic_insights.append("Path contains index out of range risk")
        if 'negative-check' in tags:
            semantic_insights.append("Path checks for negative values")
        if 'zero-check' in tags:
            semantic_insights.append("Path checks for zero values")
        
        summary['semantic_insights'] = semantic_insights
        
        return summary
    
    def analyze_path(self, predicates: List[Dict[str, Any]], 
                     trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Complete analysis of a path including tags and summary."""
        # Extract tags from predicates
        predicate_tags = self.extract_tags_from_predicates(predicates)
        
        # Combine with trace tags if available
        all_tags = set(predicate_tags)
        trace_analysis = {}
        
        if trace:
            trace_tags_info = self.extract_tags_from_trace(trace)
            trace_tags = set(trace_tags_info.get('semantic_tags', []))
            all_tags.update(trace_tags)
            trace_analysis = trace_tags_info
        
        # Generate summary
        summary = {}
        if trace:
            summary = self.generate_summary(trace, all_tags)
        
        return {
            'semantic_tags': list(all_tags),
            'tag_count': len(all_tags),
            'predicate_tags': list(predicate_tags),
            'trace_analysis': trace_analysis,
            'summary': summary,
            'path_characteristics': {
                'has_exception': 'exception-path' in all_tags,
                'has_division_risk': 'division-by-zero-risk' in all_tags,
                'has_index_risk': 'index-out-of-range-risk' in all_tags,
                'has_bound_check': any(t in all_tags for t in ['negative-check', 'zero-check', 'empty-string-check', 'length-bound-check']),
                'has_string_check': any(t in all_tags for t in ['contains-check', 'prefix-check', 'suffix-check'])
            }
        }


# Global instance for convenience
global_extractor = SemanticExtractor()


def extract_tags(expr: str) -> Set[str]:
    """Extract semantic tags from expression using global extractor."""
    return global_extractor.extract_tags_from_expr(expr)


def analyze_path(predicates: List[Dict[str, Any]], 
                 trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Analyze path using global extractor."""
    return global_extractor.analyze_path(predicates, trace)


def get_extractor() -> SemanticExtractor:
    """Get the global semantic extractor instance."""
    return global_extractor