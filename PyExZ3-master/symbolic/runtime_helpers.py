from .symbolic_types import SymbolicType, SymbolicInteger, SymbolicStr, SymbolicBool, SymbolicFloat

def unwrap(obj):
    """Unwrap a symbolic object to get its concrete value"""
    if isinstance(obj, SymbolicType):
        return obj.getConcrValue()
    return obj

def _se_int(x):
    """Handle int() conversion for symbolic objects"""
    if isinstance(x, SymbolicType):
        return SymbolicInteger("se", int(x.getConcrValue()), x.expr)
    return int(x)

def _se_str(x):
    """Handle str() conversion for symbolic objects"""
    if isinstance(x, SymbolicType):
        return SymbolicStr("se", str(x.getConcrValue()), x.expr)
    return str(x)

def _se_float(x):
    """Handle float() conversion for symbolic objects"""
    if isinstance(x, SymbolicType):
        return SymbolicFloat("se", float(x.getConcrValue()), x.expr)
    return float(x)

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

def _branch_hook(condition, line, col):
    """Hook for branch conditions to capture location information"""
    import inspect
    # Get the current frame to get the filename
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    
    # Store the location information in thread-local storage
    _local.branch_location = (filename, line, col)
    
    return condition
