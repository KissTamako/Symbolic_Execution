from ast import Call, Constant, Import, Name, If, While, NodeTransformer, fix_missing_locations, parse
import importlib, importlib.util, inspect, sys, types

class SymbolicWrapperCall(NodeTransformer):
    def visit_Call(self, node):
        for i in range(len(node.args)):
            node.args[i] = SymbolicWrapperCall().visit(node.args[i])
        if isinstance(node.func, Name):
            if node.func.id == 'int':
                if len(node.args) == 1:
                    call = parse('_se_int()').body[0].value
                    call.args = node.args
                    # Copy location information
                    call.lineno = node.lineno
                    call.col_offset = node.col_offset
                    return call
            if node.func.id == 'str':
                if len(node.args) == 1:
                    call = parse('_se_str()').body[0].value
                    call.args = node.args
                    # Copy location information
                    call.lineno = node.lineno
                    call.col_offset = node.col_offset
                    return call
            if node.func.id == 'float':
                if len(node.args) == 1:
                    call = parse('_se_float()').body[0].value
                    call.args = node.args
                    # Copy location information
                    call.lineno = node.lineno
                    call.col_offset = node.col_offset
                    return call
            if node.func.id == 'range':
                call = parse('_se_range()').body[0].value
                call.args = node.args
                # Copy location information
                call.lineno = node.lineno
                call.col_offset = node.col_offset
                return call
        return node

class SymbolicWrapperBranch(NodeTransformer):
    def visit_If(self, node):
        # Add branch hook to condition
        node.test = self._add_branch_hook(node.test, node.lineno, node.col_offset)
        return node
    
    def visit_While(self, node):
        # Add branch hook to condition
        node.test = self._add_branch_hook(node.test, node.lineno, node.col_offset)
        return node
    
    def _add_branch_hook(self, condition, line, col):
        # Create a wrapper that adds branch location information
        hook_call = parse('symbolic.runtime_helpers._branch_hook()').body[0].value
        hook_call.args = [condition, line, col]
        # Copy location information
        hook_call.lineno = line
        hook_call.col_offset = col
        return hook_call

class SymbolicWrapperConstant(NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            call = parse('symbolic.symbolic_types.SymbolicBool()').body[0].value
            call.args = [node]
            # Copy location information
            call.lineno = node.lineno
            call.col_offset = node.col_offset
            return call
        if isinstance(node.value, int):
            call = parse('symbolic.symbolic_types.SymbolicInteger()').body[0].value
            call.args = [node]
            # Copy location information
            call.lineno = node.lineno
            call.col_offset = node.col_offset
            return call
        if isinstance(node.value, float):
            call = parse('symbolic.symbolic_types.SymbolicFloat()').body[0].value
            call.args = [node]
            # Copy location information
            call.lineno = node.lineno
            call.col_offset = node.col_offset
            return call
        if isinstance(node.value, str):
            call = parse('symbolic.symbolic_types.SymbolicStr()').body[0].value
            call.args = [node]
            # Copy location information
            call.lineno = node.lineno
            call.col_offset = node.col_offset
            return call
        return node

def _exec_module(self, module):
    tree = parse(inspect.getsource(module))
    
    # Insert imports for runtime helpers
    i = 0
    while i < len(tree.body) and hasattr(tree.body[i], 'module') and tree.body[i].module == '__future__':
        i += 1
    
    from ast import alias
    tree.body.insert(i, Import(names=[alias(name='symbolic.runtime_helpers', asname=None)]))
    tree.body.insert(i, Import(names=[alias(name='symbolic.symbolic_types', asname=None)]))
    
    tree = SymbolicWrapperCall().visit(tree)
    tree = SymbolicWrapperConstant().visit(tree)
    tree = SymbolicWrapperBranch().visit(tree)
    
    # Ensure all nodes have necessary fields
    fix_missing_locations(tree)
    
    # Try to compile with error handling
    try:
        code = compile(tree, module.__file__, 'exec')
        importlib._bootstrap._call_with_frames_removed(exec, code, module.__dict__)
    except Exception as e:
        # If compilation fails, skip transformation for this module
        # import traceback
        # traceback.print_exc()
        # Fall back to original execution
        original_code = inspect.getsource(module)
        importlib._bootstrap._call_with_frames_removed(exec, original_code, module.__dict__)

def _find_spec(cls, fullname, path=None, target=None):
    spec = cls.find_spec_original(fullname, path, target)
    if not spec:
        return spec
    # Skip transformation for third-party modules and built-in modules
    if not fullname.startswith('symbolic') and not fullname.startswith('test'):
        return spec
    module = importlib.util.module_from_spec(spec)
    try:
        inspect.getsource(module)
        spec.loader.exec_module = types.MethodType(_exec_module, spec.loader)
    except Exception as e:
        msg = str(e)
        if not (isinstance(e, OSError) and msg in ('could not get source code', 'source code not available')) and not (isinstance(e, TypeError) and msg.endswith('is a built-in module')):
            import traceback
            traceback.print_exc()
            sys.exit(1)
    return spec

def install_import_hook():
    for e in sys.meta_path:
        if hasattr(e, 'find_spec'):
            e.find_spec_original = e.find_spec
            e.find_spec = types.MethodType(_find_spec, e)
    
    importlib.util.spec_from_file_location_original = importlib.util.spec_from_file_location
    
    def _spec_from_file_location(name, location=None, *, loader=None, submodule_search_locations=object()):
        spec = importlib.util.spec_from_file_location_original(name, location, loader=loader, submodule_search_locations=submodule_search_locations)
        if not spec:
            return spec
        # Skip transformation for third-party modules and built-in modules
        if not name.startswith('symbolic') and not name.startswith('test'):
            return spec
        module = importlib.util.module_from_spec(spec)
        try:
            inspect.getsource(module)
            spec.loader.exec_module = types.MethodType(_exec_module, spec.loader)
        except Exception as e:
            msg = str(e)
            if not (isinstance(e, OSError) and msg in ('could not get source code', 'source code not available')) and not (isinstance(e, TypeError) and msg.endswith('is a built-in module')):
                import traceback
                traceback.print_exc()
                sys.exit(1)
        return spec
    
    importlib.util.spec_from_file_location = _spec_from_file_location
