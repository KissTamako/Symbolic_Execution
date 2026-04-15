class SemanticExtractor:
    def extract_semantic_tags(self, path):
        """Extract semantic tags from a path"""
        tags = []
        predicates = path.get_current_path()
        
        for pred in predicates:
            expr_str = pred.toString()
            
            # Negative check
            if "< 0" in expr_str or "<= -1" in expr_str:
                tags.append("negative-check")
            
            # Zero check
            if "== 0" in expr_str or "!= 0" in expr_str:
                tags.append("zero-check")
            
            # Empty string check
            if "== ''" in expr_str or "!= ''" in expr_str:
                tags.append("empty-string-check")
            
            # Length bound check
            if "len" in expr_str and ("<" in expr_str or ">" in expr_str or "<=" in expr_str or ">=" in expr_str):
                tags.append("length-bound-check")
            
            # Contains check
            if "in" in expr_str:
                tags.append("contains-check")
            
            # Prefix check
            if "startswith" in expr_str:
                tags.append("prefix-check")
            
            # Suffix check
            if "endswith" in expr_str:
                tags.append("suffix-check")
            
            # Division by zero risk
            if "/" in expr_str or "//" in expr_str:
                tags.append("division-by-zero-risk")
            
            # Index out of range risk
            if "[" in expr_str and "]" in expr_str:
                tags.append("index-out-of-range-risk")
        
        return list(set(tags))  # Remove duplicates
    
    def generate_execution_summary(self, path, return_value, exception):
        """Generate execution summary"""
        predicates = path.get_current_path()
        summary = {
            "key_judgments": [p.toString() for p in predicates],
            "return_value": return_value,
            "exception": str(exception) if exception else None,
            "source_locations": [(p.source_file, p.source_line) for p in predicates if p.source_file and p.source_line]
        }
        return summary
