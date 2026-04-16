import ast
import os


CALL_WRAPPERS = {
    "input": "_se_input",
    "int": "_se_int",
    "str": "_se_str",
    "float": "_se_float",
    "range": "_se_range",
}


class SymbolicWrapperCall(ast.NodeTransformer):
    def visit_Call(self, node):
        node = self.generic_visit(node)
        if isinstance(node.func, ast.Name):
            helper_name = CALL_WRAPPERS.get(node.func.id)
            if helper_name:
                wrapped_call = ast.Call(
                    func=ast.Name(id=helper_name, ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords,
                )
                return ast.copy_location(wrapped_call, node)
        return node


class SymbolicWrapperBranch(ast.NodeTransformer):
    def __init__(self, filename=None):
        self.filename = filename

    def visit_If(self, node):
        node = self.generic_visit(node)
        node.test = self._add_branch_hook(node.test, node.lineno, node.col_offset)
        return node

    def visit_While(self, node):
        node = self.generic_visit(node)
        node.test = self._add_branch_hook(node.test, node.lineno, node.col_offset)
        return node

    def _add_branch_hook(self, condition, line, col):
        normalized_filename = None
        if self.filename:
            normalized_filename = os.path.normpath(self.filename).replace("\\", "/")

        branch_hook = ast.Call(
            func=ast.Name(id="_se_branch_hook", ctx=ast.Load()),
            args=[
                condition,
                ast.Constant(value=line),
                ast.Constant(value=col),
                ast.Constant(value=normalized_filename),
            ],
            keywords=[],
        )
        return ast.copy_location(branch_hook, condition)


class SymbolicWrapperConstant(ast.NodeTransformer):
    def visit_Constant(self, node):
        return node
