from ast import ImportFrom, alias, fix_missing_locations, parse

from .ast_transform import SymbolicWrapperBranch, SymbolicWrapperCall, SymbolicWrapperConstant


class ScriptInvocation:
    def __init__(self, script_path, reset):
        self.script_path = script_path
        self.reset = reset
        self.inputs = {}
        self.initial_value = {}
        self.input_types = {}
        self.input_sequence = []

    def add_input(self, name, value, input_type="int"):
        self.inputs[name] = value
        self.initial_value[name] = value
        self.input_types[name] = input_type
        self.input_sequence.append((name, value, input_type))

    def execute(self, symbolic_inputs):
        self.reset()

        from symbolic.runtime_helpers import (
            _branch_hook,
            _se_float,
            _se_input,
            _se_safe_eval,
            _se_literal_eval,
            _se_int,
            _se_range,
            _se_str,
            init_symbolic_inputs,
            set_current_file_path,
        )

        ordered_inputs = []
        for name, default_value, input_type in self.input_sequence:
            ordered_inputs.append((name, symbolic_inputs.get(name, default_value), input_type))
        init_symbolic_inputs(ordered_inputs)

        local_vars = {
            "__name__": "__main__",
            "__file__": self.script_path,
            "_se_branch_hook": _branch_hook,
            "_se_input": _se_input,
            "_se_safe_eval": _se_safe_eval,
            "_se_literal_eval": _se_literal_eval,
            "_se_int": _se_int,
            "_se_str": _se_str,
            "_se_float": _se_float,
            "_se_range": _se_range,
        }
        local_vars.update(symbolic_inputs)

        try:
            set_current_file_path(self.script_path)

            with open(self.script_path, "r", encoding="utf-8") as file_obj:
                script_content = file_obj.read()

            tree = parse(script_content, filename=self.script_path)

            insert_at = 0
            while (
                insert_at < len(tree.body)
                and hasattr(tree.body[insert_at], "module")
                and tree.body[insert_at].module == "__future__"
            ):
                insert_at += 1

            tree.body.insert(
                insert_at,
                ImportFrom(
                    module="symbolic.runtime_helpers",
                    names=[
                        alias(name="_branch_hook", asname="_se_branch_hook"),
                        alias(name="_se_input", asname=None),
                        alias(name="_se_safe_eval", asname=None),
                        alias(name="_se_literal_eval", asname=None),
                        alias(name="_se_int", asname=None),
                        alias(name="_se_str", asname=None),
                        alias(name="_se_float", asname=None),
                        alias(name="_se_range", asname=None),
                    ],
                    level=0,
                ),
            )

            tree = SymbolicWrapperCall().visit(tree)
            tree = SymbolicWrapperConstant().visit(tree)
            tree = SymbolicWrapperBranch(filename=self.script_path).visit(tree)
            fix_missing_locations(tree)

            code = compile(tree, self.script_path, "exec")
            exec(code, local_vars)
            return None
        finally:
            set_current_file_path(None)

    def getNames(self):
        return self.inputs.keys()

    def createArgumentValue(self, name, val=None):
        from .symbolic_types import SymbolicFloat, SymbolicInteger, SymbolicStr

        if val is None:
            val = self.initial_value[name]

        input_type = self.input_types.get(name, "int")
        if input_type == "eval_input":
            # eval_input 需要一个可以被 eval 的字符串作为默认值
            # 使用 "0" 作为默认值
            return SymbolicStr(name, "0")
        if input_type == "str":
            return SymbolicStr(name, val)
        if input_type == "float":
            return SymbolicFloat(name, val)
        return SymbolicInteger(name, val)


class ScriptRunner:
    def __init__(self, script_path):
        self.script_path = script_path

    def create_invocation(self):
        def reset():
            pass

        return ScriptInvocation(self.script_path, reset)
