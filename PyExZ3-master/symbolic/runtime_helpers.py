# Copyright: see copyright.txt
"""
Runtime helper functions for preserving symbolic information.

Week 1: Skeleton implementation
Week 2: Will implement actual helper functions
"""

def _se_int(x):
    """
    Wrap integer constructor to preserve symbolic information.
    
    Args:
        x: Value to convert to int
    
    Returns:
        int(x) preserving symbolic information if x is symbolic
    
    Reference PyCT implementation: _int() checks for Concolic type and calls __int2__()
    """
    # Check if x is already a symbolic integer
    from .symbolic_types.symbolic_int import SymbolicInteger
    from .symbolic_types.symbolic_type import SymbolicObject
    
    if isinstance(x, SymbolicInteger):
        # Already symbolic, preserve symbolic expression
        # Use PyCT approach: call the original int.__int__ method if available
        if hasattr(x, '__int__'):
            try:
                # Try to get concrete value through original int method
                concrete = int.__int__(x)
            except:
                concrete = int(x)
        else:
            concrete = int(x)
            
        # Check if we should preserve expression
        expr = None
        if hasattr(x, 'expr'):
            expr = x.expr
        elif hasattr(x, '_expr'):
            expr = x._expr
            
        return SymbolicInteger("se", concrete, expr or x)
    elif isinstance(x, SymbolicObject):
        # Other symbolic type, extract concrete value and create new symbolic integer
        # Try PyCT approach first: use original type methods
        if hasattr(x, '__int__'):
            try:
                concrete = int.__int__(x)
            except:
                concrete = x.getConcrValue() if hasattr(x, 'getConcrValue') else int(x)
        else:
            concrete = x.getConcrValue() if hasattr(x, 'getConcrValue') else int(x)
            
        return SymbolicInteger("se", int(concrete), x)
    else:
        # Concrete value, create new symbolic integer
        concrete = int(x)
        return SymbolicInteger("se", concrete, None)


def _se_str(x):
    """
    Wrap string constructor to preserve symbolic information.
    
    Args:
        x: Value to convert to str
    
    Returns:
        str(x) preserving symbolic information if x is symbolic
    """
    # Check if x is already a symbolic string
    from .symbolic_types.symbolic_str import SymbolicStr
    from .symbolic_types.symbolic_type import SymbolicObject
    
    if isinstance(x, SymbolicStr):
        # Already symbolic, preserve symbolic expression
        return SymbolicStr("se", str(x), x.expr if hasattr(x, 'expr') else x)
    elif isinstance(x, SymbolicObject):
        # Other symbolic type, extract concrete value and create new symbolic string
        concrete = x.getConcrValue() if hasattr(x, 'getConcrValue') else str(x)
        return SymbolicStr("se", str(concrete), x)
    else:
        # Concrete value, create new symbolic string
        concrete = str(x)
        return SymbolicStr("se", concrete, None)


def _se_range(*args):
    """
    Wrap range constructor to preserve symbolic information.
    
    Args:
        *args: Arguments to range() function
    
    Returns:
        range object preserving symbolic information if args are symbolic
    """
    # For range, we need to handle symbolic arguments
    # This is a simplified implementation - in practice we'd need
    # to create a symbolic range object
    from .symbolic_types.symbolic_int import SymbolicInteger
    from .symbolic_types.symbolic_type import SymbolicObject
    
    # Extract concrete values from arguments
    concrete_args = []
    symbolic_exprs = []
    has_symbolic = False
    
    for arg in args:
        if isinstance(arg, SymbolicObject):
            concrete = arg.getConcrValue() if hasattr(arg, 'getConcrValue') else int(arg)
            concrete_args.append(concrete)
            symbolic_exprs.append(arg)
            has_symbolic = True
        else:
            concrete_args.append(arg)
            symbolic_exprs.append(None)
    
    # Create concrete range
    range_obj = range(*concrete_args)
    
    if has_symbolic:
        # Create a symbolic wrapper for the range
        # Note: This is a simplified approach. A full implementation would
        # require a SymbolicRange class that wraps range operations.
        return range_obj
    else:
        return range_obj


def unwrap(value):
    """
    Extract concrete value from symbolic object.
    
    Args:
        value: Either a symbolic object or concrete value
    
    Returns:
        Concrete value
    
    Reference PyCT implementation: calls primitive's casting function to avoid
    getting stuck when the symbolic object's method is modified.
    """
    from .symbolic_types.symbolic_type import SymbolicObject
    from .symbolic_types.symbolic_int import SymbolicInteger
    from .symbolic_types.symbolic_str import SymbolicStr
    
    # Check for specific symbolic types first (PyCT approach)
    if isinstance(value, SymbolicInteger):
        # Use original int.__int__ method to get concrete value
        try:
            return int.__int__(value)
        except:
            if hasattr(value, 'getConcrValue'):
                return value.getConcrValue()
            return int(value)
    elif isinstance(value, SymbolicStr):
        # Use original str.__str__ method to get concrete value
        try:
            return str.__str__(value)
        except:
            if hasattr(value, 'getConcrValue'):
                return value.getConcrValue()
            return str(value)
    elif isinstance(value, SymbolicObject):
        # Generic symbolic object
        if hasattr(value, 'getConcrValue'):
            return value.getConcrValue()
        elif hasattr(value, '__int__'):
            try:
                return int.__int__(value)
            except:
                return int(value)
        elif hasattr(value, '__str__'):
            try:
                return str.__str__(value)
            except:
                return str(value)
        elif hasattr(value, '__bool__'):
            try:
                # Try to use bool.__bool__ if available
                # Reference PyCT implementation: bool.__bool__(value)
                return bool.__bool__(value)
            except:
                return bool(value)
    
    # Handle lists/tuples of symbolic objects (recursive unwrap)
    if isinstance(value, (list, tuple)):
        return type(value)(unwrap(item) for item in value)
    
    # Not a symbolic object, return as-is
    return value


def wrap_concrete_constant(value):
    """
    Wrap concrete constant to preserve potential symbolic information.
    
    Args:
        value: Concrete value
    
    Returns:
        Wrapped value that can preserve symbolic context
    """
    from .symbolic_types.symbolic_int import SymbolicInteger
    from .symbolic_types.symbolic_str import SymbolicStr
    
    if isinstance(value, bool):
        # For bool, we need to check if there's a SymbolicBool class
        # For now, return as-is since bool wrapping is not specified in requirements
        return value
    elif isinstance(value, int):
        return SymbolicInteger("const", value, None)
    elif isinstance(value, str):
        return SymbolicStr("const", value, None)
    elif isinstance(value, (list, tuple)):
        # Recursively wrap elements
        return type(value)(wrap_concrete_constant(item) for item in value)
    else:
        # Unsupported type, return as-is
        return value


class RuntimeHelperManager:
    """Manager for runtime helper functions."""
    
    def __init__(self):
        self.helpers_registered = False
    
    def register_helpers(self):
        """Register helper functions in the global namespace."""
        if not self.helpers_registered:
            # TODO: Week 2 - Actually register helpers
            self.helpers_registered = True
    
    def unregister_helpers(self):
        """Unregister helper functions from global namespace."""
        if self.helpers_registered:
            # TODO: Week 2 - Actually unregister helpers
            self.helpers_registered = False