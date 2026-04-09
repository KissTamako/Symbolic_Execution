# Copyright: see copyright.txt
"""
AST transformation module for preserving symbolic information.

Week 2: AST transformation implementation
Adapted from PyCT's wrapper.py with modifications for PyExZ3 compatibility.
"""

import ast
import importlib
import inspect
import sys
import types
from pathlib import Path

# Import symbolic types for wrapping
from .symbolic_types.symbolic_int import SymbolicInteger
from .symbolic_types.symbolic_str import SymbolicStr
from .symbolic_types.symbolic_type import SymbolicObject
from .runtime_helpers import _se_int, _se_str, _se_range, unwrap, wrap_concrete_constant


class SEConstantWrapper(ast.NodeTransformer):
    """
    Wrap constants to preserve symbolic information.
    
    Transforms:
    - 5 -> wrap_concrete_constant(5)
    - "hello" -> wrap_concrete_constant("hello")
    - True -> wrap_concrete_constant(True)
    """
    
    def visit_Constant(self, node: ast.Constant):
        # Only wrap supported types: bool, int, str
        if isinstance(node.value, (bool, int, str)):
            # Create call to wrap_concrete_constant(value)
            call = ast.Call(
                func=ast.Name(id='wrap_concrete_constant', ctx=ast.Load()),
                args=[node],
                keywords=[]
            )
            return call
        return node


class SEFunctionCallWrapper(ast.NodeTransformer):
    """
    Wrap function calls to preserve symbolic information.
    
    Transforms:
    - int(x) -> _se_int(x)
    - str(x) -> _se_str(x)
    - range(...) -> _se_range(...)
    """
    
    def visit_Call(self, node: ast.Call):
        # First transform arguments recursively
        for i in range(len(node.args)):
            node.args[i] = self.visit(node.args[i])
        
        # Transform keywords if any
        for kw in node.keywords:
            kw.value = self.visit(kw.value)
        
        # Check if this is a call to a built-in function we want to wrap
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # int(x) -> _se_int(x)
            if func_name == 'int' and len(node.args) == 1:
                return ast.Call(
                    func=ast.Name(id='_se_int', ctx=ast.Load()),
                    args=node.args,
                    keywords=[]
                )
            
            # str(x) -> _se_str(x)
            elif func_name == 'str' and len(node.args) == 1:
                return ast.Call(
                    func=ast.Name(id='_se_str', ctx=ast.Load()),
                    args=node.args,
                    keywords=[]
                )
            
            # range(...) -> _se_range(...)
            elif func_name == 'range' and 1 <= len(node.args) <= 3:
                return ast.Call(
                    func=ast.Name(id='_se_range', ctx=ast.Load()),
                    args=node.args,
                    keywords=[]
                )
        
        return node


class SEBranchHookInjector(ast.NodeTransformer):
    """
    Inject branch hooks for if/while statements to record source location.
    
    Transforms:
    - if condition: -> if __branch_hook(file, line, branch_id, condition):
    - while condition: -> while __branch_hook(file, line, branch_id, condition):
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self.branch_counter = 0
    
    def visit_If(self, node: ast.If):
        # Generate branch ID
        branch_id = self.branch_counter
        self.branch_counter += 1
        
        # Create hook call
        hook_call = ast.Call(
            func=ast.Name(id='__branch_hook', ctx=ast.Load()),
            args=[
                ast.Constant(value=self.filename),
                ast.Constant(value=node.lineno if hasattr(node, 'lineno') else 0),
                ast.Constant(value=branch_id),
                node.test
            ],
            keywords=[]
        )
        
        # Replace test with hook call
        node.test = hook_call
        
        # Process body and orelse recursively
        node.body = [self.visit(stmt) for stmt in node.body]
        if node.orelse:
            node.orelse = [self.visit(stmt) for stmt in node.orelse]
        
        return node
    
    def visit_While(self, node: ast.While):
        # Generate branch ID
        branch_id = self.branch_counter
        self.branch_counter += 1
        
        # Create hook call
        hook_call = ast.Call(
            func=ast.Name(id='__branch_hook', ctx=ast.Load()),
            args=[
                ast.Constant(value=self.filename),
                ast.Constant(value=node.lineno if hasattr(node, 'lineno') else 0),
                ast.Constant(value=branch_id),
                node.test
            ],
            keywords=[]
        )
        
        # Replace test with hook call
        node.test = hook_call
        
        # Process body and orelse recursively
        node.body = [self.visit(stmt) for stmt in node.body]
        if node.orelse:
            node.orelse = [self.visit(stmt) for stmt in node.orelse]
        
        return node


def transform_ast(source_code: str, filename: str, inject_branch_hooks: bool = False) -> ast.Module:
    """
    Transform Python source code AST to preserve symbolic information.
    
    Args:
        source_code: Python source code
        filename: Source filename for error reporting
        inject_branch_hooks: Whether to inject branch hooks
    
    Returns:
        Transformed AST module
    """
    # Parse source code
    tree = ast.parse(source_code, filename=filename)
    
    # Apply transformations in order
    transformers = []
    
    # 1. Wrap constants
    transformers.append(SEConstantWrapper())
    
    # 2. Wrap function calls
    transformers.append(SEFunctionCallWrapper())
    
    # 3. Inject branch hooks if requested
    if inject_branch_hooks:
        transformers.append(SEBranchHookInjector(filename))
    
    # Apply all transformations
    for transformer in transformers:
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)
    
    return tree


def compile_transformed_module(tree: ast.Module, module_name: str) -> types.CodeType:
    """
    Compile transformed AST module to code object.
    
    Args:
        tree: Transformed AST module
        module_name: Name of the module
    
    Returns:
        Compiled code object
    """
    return compile(tree, filename=module_name, mode='exec')


def branch_hook(filename: str, line: int, branch_id: int, condition) -> bool:
    """
    Branch hook function to record branch information.
    
    Args:
        filename: Source filename
        line: Line number
        branch_id: Branch identifier
        condition: Branch condition value
    
    Returns:
        The condition value (passed through)
    """
    # This hook will be called by injected code
    # Actual branch recording happens in SymbolicObject.__bool__
    # This just provides metadata
    from .trace import record_branch
    record_branch(filename, line, branch_id, condition)
    return bool(condition)


def setup_branch_hook_globals(globals_dict: dict):
    """
    Setup branch hook function in globals dict.
    
    Args:
        globals_dict: Globals dictionary to update
    """
    globals_dict['__branch_hook'] = branch_hook
    globals_dict['wrap_concrete_constant'] = wrap_concrete_constant
    globals_dict['_se_int'] = _se_int
    globals_dict['_se_str'] = _se_str
    globals_dict['_se_range'] = _se_range
    globals_dict['unwrap'] = unwrap