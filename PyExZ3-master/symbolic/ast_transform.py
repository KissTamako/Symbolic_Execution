from ast import Call, Constant, Import, Name, If, While, NodeTransformer, fix_missing_locations, parse, Load

class SymbolicWrapperCall(NodeTransformer):
    def visit_Call(self, node):
        for i in range(len(node.args)):
            node.args[i] = SymbolicWrapperCall().visit(node.args[i])
        if isinstance(node.func, Name):
            # 处理 input() 调用
            if node.func.id == 'input':
                call = parse('_se_input()').body[0].value
                call.args = node.args
                return call
        # 不再替换其他函数调用，保持原样
        return node

class SymbolicWrapperBranch(NodeTransformer):
    def __init__(self, filename=None):
        self.filename = filename
    
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
        filename = self.filename
        if not filename:
            # Try to get filename from caller
            import inspect
            frame = inspect.currentframe()
            while frame:
                if 'ast_transform.py' not in frame.f_code.co_filename:
                    filename = frame.f_code.co_filename
                    break
                frame = frame.f_back
        
        # 使用 __import__ 来获取 symbolic 模块，避免名称冲突
        from ast import Call, Name, Attribute, Subscript, Str
        
        # 创建 __import__('symbolic') 获取 symbolic 模块
        import_call = Call(
            func=Name(id='__import__', ctx=Load()),
            args=[Str(s='symbolic')],
            keywords=[]
        )
        
        # 创建 branch_hook 调用
        branch_hook = Call(
            func=Attribute(
                value=Attribute(
                    value=import_call,
                    attr='runtime_helpers',
                    ctx=Load()
                ),
                attr='_branch_hook',
                ctx=Load()
            ),
            args=[condition, parse(f'{line}').body[0].value, parse(f'{col}').body[0].value, parse(f'"{filename}"').body[0].value],
            keywords=[]
        )
        
        return branch_hook

class SymbolicWrapperConstant(NodeTransformer):
    def visit_Constant(self, node):
        # Do not wrap constants - let wrap_concrete_constant handle at runtime
        return node