import os

from .symbolic_types import SymbolicType, SymbolicInteger, SymbolicStr, SymbolicBool, SymbolicFloat

def unwrap(obj):
    """Unwrap a symbolic object to get its concrete value"""
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
    """Handle range() for symbolic objects"""
    # For now, we'll just use concrete values
    # TODO: Implement symbolic range support
    concrete_args = [unwrap(arg) for arg in args]
    return range(*concrete_args)

def wrap_concrete_constant(value):
    """Wrap a concrete constant in a symbolic type if appropriate"""
    from .symbolic_types import getSymbolic
    sym_type = getSymbolic(value)
    if sym_type:
        return sym_type("const", value)
    return value

# Create a module-level thread-local storage
import threading
_local = threading.local()

# Also create a thread-local storage for file path
_file_path_local = threading.local()

# Thread-local storage for symbolic inputs
_input_local = threading.local()

def init_symbolic_inputs(inputs):
    """Initialize symbolic inputs for script mode"""
    _input_local.inputs = inputs
    _input_local.input_index = 0

def get_next_symbolic_input():
    """Get the next symbolic input in sequence"""
    if not hasattr(_input_local, 'inputs') or not hasattr(_input_local, 'input_index'):
        # 没有初始化符号输入，回退到真实 input()
        return input()
    
    if _input_local.input_index >= len(_input_local.inputs):
        # 输入序列用完了，回退到真实 input()
        return input()
    
    # 支持包含类型信息的输入序列
    input_item = _input_local.inputs[_input_local.input_index]
    _input_local.input_index += 1
    
    if len(input_item) == 3:
        # 包含类型信息的格式: (name, value, type)
        input_name, input_value, input_type = input_item
        return input_value
    else:
        # 旧格式: (name, value)
        input_name, input_value = input_item
        return input_value

def _se_input(prompt=""):
    """Handle input() calls with symbolic inputs"""
    # If prompt is provided, print it (like real input())
    if prompt:
        print(prompt, end='')
    
    # Get the next symbolic input
    try:
        return get_next_symbolic_input()
    except RuntimeError:
        # Fall back to real input if no symbolic inputs available
        return input(prompt)

# Set the current file path
def set_current_file_path(file_path):
    _file_path_local.file_path = file_path

# Get the current file path
def get_current_file_path():
    return getattr(_file_path_local, 'file_path', None)

def _branch_hook(condition, line, col, filename=None):
    """Hook for branch conditions to capture location information"""
    import inspect
    
    # 如果没有提供文件名，尝试从 thread-local storage 获取
    if not filename:
        filename = get_current_file_path()
    
    # 如果仍然没有文件名，尝试从调用栈中获取
    if not filename:
        # 遍历调用栈，找到第一个不是 runtime_helpers.py 和 symbolic_types 目录下的文件的帧
        frame = inspect.currentframe()
        while frame:
            filename = frame.f_code.co_filename
            if 'runtime_helpers.py' not in filename and 'symbolic_types' not in filename:
                break
            frame = frame.f_back
    
    # Store the location information in thread-local storage
    if filename:
        filename = os.path.normpath(filename).replace("\\", "/")
    _local.branch_location = (filename, line, col)
    
    return condition
