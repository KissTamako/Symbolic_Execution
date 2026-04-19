import os
import threading

from .symbolic_types import (
    SymbolicBool,
    SymbolicFloat,
    SymbolicInteger,
    SymbolicStr,
    SymbolicType,
)


class SymbolicDynamicValue(SymbolicType):
    """Symbolic value that can dynamically change type based on context."""
    def __init__(self, name, raw_input, concrete_value, type_tag=None):
        super().__init__(name, concrete_value)
        self.raw_input = raw_input
        self.type_tag = type_tag

    def getRawInput(self):
        return self.raw_input

    def getTypeTag(self):
        return self.type_tag

    def setTypeTag(self, type_tag):
        self.type_tag = type_tag

    def getConcrValue(self):
        return self.expr

    def __iter__(self):
        """Make the object iterable if its concrete value is iterable."""
        concrete = self.expr
        if isinstance(concrete, (list, tuple, set, str)):
            return iter(concrete)
        raise TypeError(f"'{type(concrete).__name__}' object is not iterable")

    def __len__(self):
        """Return the length of the concrete value."""
        concrete = self.expr
        if isinstance(concrete, (list, tuple, set, str)):
            return len(concrete)
        raise TypeError(f"object of type '{type(concrete).__name__}' has no len()")

    def __getitem__(self, key):
        """Allow indexing if the concrete value supports it."""
        concrete = self.expr
        if isinstance(concrete, (list, tuple, str)):
            return concrete[key]
        raise TypeError(f"'{type(concrete).__name__}' object is not subscriptable")

    def __bool__(self):
        """Return True if the concrete value is truthy."""
        return bool(self.expr)


def unwrap(obj):
    """Unwrap a symbolic object to get its concrete value."""
    if isinstance(obj, SymbolicType):
        return obj.getConcrValue()
    return obj


def _se_int(*args, **kwargs):
    """Handle int() conversion while preserving symbolic expressions when possible."""
    if len(args) == 1 and not kwargs and isinstance(args[0], SymbolicType):
        symbolic_value = args[0]
        if hasattr(symbolic_value, "__int2__"):
            return symbolic_value.__int2__()
        return SymbolicInteger("se", int(symbolic_value.getConcrValue()), symbolic_value.expr)
    return int(*args, **kwargs)


def _se_str(*args, **kwargs):
    """Handle str() conversion while preserving symbolic expressions when possible."""
    if len(args) == 1 and not kwargs and isinstance(args[0], SymbolicType):
        symbolic_value = args[0]
        if hasattr(symbolic_value, "__str2__"):
            return symbolic_value.__str2__()
        return SymbolicStr("se", str(symbolic_value.getConcrValue()), symbolic_value.expr)
    return str(*args, **kwargs)


def _se_float(*args, **kwargs):
    """Handle float() conversion while preserving symbolic expressions when possible."""
    if len(args) == 1 and not kwargs and isinstance(args[0], SymbolicType):
        symbolic_value = args[0]
        if hasattr(symbolic_value, "__float2__"):
            return symbolic_value.__float2__()
        return SymbolicFloat("se", float(symbolic_value.getConcrValue()), symbolic_value.expr)
    return float(*args, **kwargs)


def _se_range(*args):
    """Handle range() for symbolic objects."""
    concrete_args = [unwrap(arg) for arg in args]
    return range(*concrete_args)


def _se_literal_eval(raw):
    """Handle literal evaluation of input values for eval(input()) pattern.

    This function is specifically designed to handle the pattern eval(input())
    by safely evaluating the input as a literal and returning the concrete value.
    """
    # 获取原始输入的具体值
    if isinstance(raw, SymbolicType):
        raw_input = raw.getConcrValue()
    else:
        raw_input = raw

    # 确保输入是字符串
    if not isinstance(raw_input, str):
        raw_input = str(raw_input)

    # 默认为空字符串时返回 0
    if raw_input == '':
        return 0

    # 尝试进行字面量求值
    try:
        concrete_value = eval(raw_input)
    except Exception:
        # 如果求值失败，返回原始输入
        concrete_value = raw_input

    # 返回具体的值
    return concrete_value


def _se_safe_eval(expr):
    """Handle eval() calls with symbolic inputs.

    When expr is a SymbolicType, we cannot actually evaluate it meaningfully
    in the symbolic execution context, so we return it as-is to preserve
    the symbolic value. This handles the common pattern eval(input())
    where input() has been replaced with _se_input().
    """
    # Check if expr is a symbolic type and get its concrete value if available
    if isinstance(expr, SymbolicType):
        conc_value = expr.getConcrValue()
        if conc_value is not None:
            expr = conc_value
        else:
            return expr

    if isinstance(expr, str):
        if expr == '':
            return 0
        try:
            result = eval(expr)
            return result
        except Exception:
            return expr
    return eval(expr)


def wrap_concrete_constant(value):
    """Wrap a concrete constant in a symbolic type if appropriate."""
    from .symbolic_types import getSymbolic

    sym_type = getSymbolic(value)
    if sym_type:
        return sym_type("const", value)
    return value


_local = threading.local()
_file_path_local = threading.local()
_input_local = threading.local()


def _default_value_for_input_type(input_type):
    if input_type == "str":
        return ""
    if input_type == "float":
        return 0.0
    if input_type == "bool":
        return False
    return 0


def _coerce_symbolic_input(name, input_value, input_type=None):
    if isinstance(input_value, SymbolicType):
        return input_value

    inferred_type = input_type
    if inferred_type is None:
        if isinstance(input_value, str):
            inferred_type = "str"
        elif isinstance(input_value, float):
            inferred_type = "float"
        elif isinstance(input_value, bool):
            inferred_type = "bool"
        else:
            inferred_type = "int"

    if input_value is None:
        input_value = _default_value_for_input_type(inferred_type)

    if inferred_type == "str":
        return SymbolicStr(name, str(input_value))
    if inferred_type == "float":
        return SymbolicFloat(name, float(input_value))
    if inferred_type == "bool":
        return SymbolicBool(name, bool(input_value))
    return SymbolicInteger(name, int(input_value))


def _normalize_input_item(input_item, index):
    if isinstance(input_item, SymbolicType):
        return input_item

    if isinstance(input_item, (list, tuple)):
        if len(input_item) == 3:
            input_name, input_value, input_type = input_item
            return _coerce_symbolic_input(input_name, input_value, input_type)
        if len(input_item) == 2:
            input_name, input_value = input_item
            return _coerce_symbolic_input(input_name, input_value)
        if len(input_item) == 1:
            return _coerce_symbolic_input(f"input_{index}", input_item[0])
        raise ValueError(f"Unsupported symbolic input tuple: {input_item!r}")

    return input_item


def init_symbolic_inputs(inputs):
    """Initialize symbolic inputs for script mode."""
    normalized_inputs = []
    for index, input_item in enumerate(inputs or []):
        normalized_inputs.append(_normalize_input_item(input_item, index))
    _input_local.inputs = normalized_inputs
    _input_local.input_index = 0


def get_next_symbolic_input():
    """Get the next symbolic input in sequence."""
    if not hasattr(_input_local, "inputs") or not hasattr(_input_local, "input_index"):
        return input()

    if _input_local.input_index >= len(_input_local.inputs):
        return input()

    input_item = _input_local.inputs[_input_local.input_index]
    _input_local.input_index += 1
    return input_item


def _se_input(prompt=""):
    """Handle input() calls with symbolic inputs."""
    if prompt:
        print(prompt, end="")

    try:
        return get_next_symbolic_input()
    except RuntimeError:
        return input(prompt)


def set_current_file_path(file_path):
    _file_path_local.file_path = file_path


def get_current_file_path():
    return getattr(_file_path_local, "file_path", None)


def _se_eval_numeric_input(raw):
    """Handle eval(input()) in numeric contexts (arithmetic operations)."""
    value = _se_literal_eval(raw)
    if isinstance(value, SymbolicDynamicValue):
        value.setTypeTag("numeric")
    return value


def _se_eval_sequence_input(raw):
    """Handle eval(input()) in sequence contexts (len(), indexing, iteration)."""
    value = _se_literal_eval(raw)
    if isinstance(value, SymbolicDynamicValue):
        value.setTypeTag("sequence")
    return value


def _se_eval_digit_char(raw):
    """Handle eval(input()) for single digit/char inputs."""
    value = _se_literal_eval(raw)
    if isinstance(value, SymbolicDynamicValue):
        value.setTypeTag("digit_char")
    return value


def _branch_hook(condition, line, col, filename=None):
    """Hook for branch conditions to capture location information."""
    import inspect

    if not filename:
        filename = get_current_file_path()

    if not filename:
        frame = inspect.currentframe()
        while frame:
            filename = frame.f_code.co_filename
            if "runtime_helpers.py" not in filename and "symbolic_types" not in filename:
                break
            frame = frame.f_back

    if filename:
        filename = os.path.normpath(filename).replace("\\", "/")
    _local.branch_location = (filename, line, col)

    return condition
