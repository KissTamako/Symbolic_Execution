class InputModel:
    def __init__(self):
        self.inputs = []
    
    def add_input(self, name, input_type, default=None, min_value=None, max_value=None, max_len=None):
        """Add an input specification"""
        input_spec = {
            "name": name,
            "type": input_type,
            "default": default,
            "min": min_value,
            "max": max_value,
            "max_len": max_len
        }
        self.inputs.append(input_spec)
    
    def get_inputs(self):
        """Get all input specifications"""
        return self.inputs
    
    def from_json(self, json_str):
        """Load input model from JSON string"""
        import json
        data = json.loads(json_str)
        self.inputs = data.get("inputs", [])
    
    def from_file(self, file_path):
        """Load input model from file"""
        import json
        with open(file_path, "r") as f:
            data = json.load(f)
        self.inputs = data.get("inputs", [])
