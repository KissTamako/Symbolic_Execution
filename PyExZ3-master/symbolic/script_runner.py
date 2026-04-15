import os
import sys

class ScriptInvocation:
    def __init__(self, script_path, reset):
        self.script_path = script_path
        self.reset = reset
        self.inputs = {}
    
    def add_input(self, name, value):
        """Add an input for the script"""
        self.inputs[name] = value
    
    def execute(self, symbolic_inputs):
        """Execute the script"""
        self.reset()
        
        # Set up environment with symbolic inputs
        for name, value in symbolic_inputs.items():
            globals()[name] = value
        
        # Execute the script
        try:
            exec(open(self.script_path).read(), globals())
            return None  # Scripts typically don't return values
        except Exception as e:
            return e

class ScriptRunner:
    def __init__(self, script_path):
        self.script_path = script_path
    
    def create_invocation(self):
        """Create a script invocation"""
        def reset():
            # Reset module state
            pass
        return ScriptInvocation(self.script_path, reset)
