import os
import sys
from ast import parse, fix_missing_locations, Import, alias
from .ast_transform import SymbolicWrapperCall, SymbolicWrapperBranch, SymbolicWrapperConstant

class ScriptInvocation:
    def __init__(self, script_path, reset):
        self.script_path = script_path
        self.reset = reset
        self.inputs = {}
        self.initial_value = {}
        self.input_sequence = []  # 存储输入序列，用于 input() 调用的顺序分配
    
    def add_input(self, name, value):
        """Add an input for the script"""
        self.inputs[name] = value
        self.initial_value[name] = value
        self.input_sequence.append((name, value))  # 同时添加到输入序列
    
    def execute(self, symbolic_inputs):
        """Execute the script with AST transformation"""
        self.reset()
        
        # 初始化符号输入序列
        from symbolic.runtime_helpers import init_symbolic_inputs
        # 使用 input_sequence 而不是 symbolic_inputs，以保持顺序
        init_symbolic_inputs(self.input_sequence)
        
        # Set up environment with symbolic inputs
        local_vars = {}
        for name, value in symbolic_inputs.items():
            local_vars[name] = value
        
        # Add necessary imports to local variables
        import symbolic.runtime_helpers
        import symbolic.symbolic_types
        local_vars['symbolic'] = symbolic
        local_vars['_se_int'] = symbolic.symbolic_types.SymbolicInteger
        local_vars['_se_str'] = symbolic.symbolic_types.SymbolicStr
        local_vars['_se_float'] = symbolic.symbolic_types.SymbolicFloat
        local_vars['_se_range'] = range  # Use regular range for now
        local_vars['_se_input'] = symbolic.runtime_helpers._se_input
        
        # Execute the script
        try:
            # Read the script content
            with open(self.script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Parse script into AST
            tree = parse(script_content, filename=self.script_path)
            
            # Insert necessary imports
            i = 0
            while i < len(tree.body) and hasattr(tree.body[i], 'module') and tree.body[i].module == '__future__':
                i += 1
            
            tree.body.insert(i, Import(names=[alias(name='symbolic.runtime_helpers', asname=None)]))
            tree.body.insert(i, Import(names=[alias(name='symbolic.symbolic_types', asname=None)]))
            
            # Apply the same AST transformations as function mode
            tree = SymbolicWrapperCall().visit(tree)
            tree = SymbolicWrapperConstant().visit(tree)
            tree = SymbolicWrapperBranch(filename=self.script_path).visit(tree)
            
            # Fix missing locations
            fix_missing_locations(tree)
            
            # Compile and execute with transformed AST
            code = compile(tree, self.script_path, 'exec')
            exec(code, local_vars)
            
            return None  # Scripts typically don't return values
        except Exception as e:
            import traceback
            traceback.print_exc()
            return e
    
    def getNames(self):
        """Get the names of the inputs"""
        return self.inputs.keys()
    
    def createArgumentValue(self, name, val=None):
        """Create a symbolic argument value"""
        from .symbolic_types import SymbolicInteger
        if val is None:
            val = self.initial_value[name]
        return SymbolicInteger(name, val)

class ScriptRunner:
    def __init__(self, script_path):
        self.script_path = script_path
    
    def create_invocation(self):
        """Create a script invocation"""
        def reset():
            # Reset module state
            pass
        return ScriptInvocation(self.script_path, reset)