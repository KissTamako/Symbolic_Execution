import json
import os

class CorpusExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def export_corpus(self, program_id, submission_id, paths, semantic_tags_list):
        """Export corpus data for clustering"""
        corpus_path = os.path.join(self.output_dir, "corpus.jsonl")
        
        with open(corpus_path, "w") as f:
            for i, (path, semantic_tags) in enumerate(zip(paths, semantic_tags_list)):
                path_data = path.get_current_path()
                corpus_entry = {
                    "program_id": program_id,
                    "submission_id": submission_id,
                    "path_id": i,
                    "inputs": {},  # TODO: Add input data
                    "raw_pc": [p.toString() for p in path_data],
                    "normalized_pc": [],  # TODO: Add normalized constraints
                    "branch_trace": [p.result for p in path_data],
                    "semantic_tags": semantic_tags,
                    "outcome": "success",  # TODO: Determine outcome
                    "coverage_delta": 0  # TODO: Calculate coverage delta
                }
                f.write(json.dumps(corpus_entry) + "\n")
        
        return corpus_path
