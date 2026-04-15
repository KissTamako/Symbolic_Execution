from . symbolic_type import SymbolicObject

class SymbolicBool(SymbolicObject):

    def __init__(self, name, v, expr=None):
        SymbolicObject.__init__(self, name, expr)
        self.val = bool(v)

    def getConcrValue(self):
        return self.val

    def wrap(conc, sym):
        return SymbolicBool("se", conc, sym)

    def __hash__(self):
        return hash(self.val)

    def _op_worker(self, args, fun, op, wrap=None):
        if wrap is None:
            wrap = SymbolicBool.wrap
        return self._do_sexpr(args, fun, op, wrap)

    def __bool__(self):
        ret = bool(self.getConcrValue())
        if SymbolicObject.SI != None:
            SymbolicObject.SI.whichBranch(ret, self)
        return ret

# Boolean operations

# Not operation
def __not__(self):
    return self._op_worker([self], lambda x: not x, "not")

# And operation
def __and__(self, other):
    return self._op_worker([self, other], lambda x, y: x and y, "and")

# Or operation
def __or__(self, other):
    return self._op_worker([self, other], lambda x, y: x or y, "or")

# Xor operation
def __xor__(self, other):
    return self._op_worker([self, other], lambda x, y: x ^ y, "xor")

# Add operation (bool + other)
def __add__(self, other):
    if hasattr(other, '__radd__'):
        return other.__radd__(self)
    return self.val + other

# Helper methods

def __bool2__(self):
    return self

def __float2__(self):
    from . symbolic_float import SymbolicFloat
    value = float(self.val)
    expr = ["ite", self, 1.0, 0.0]
    return SymbolicFloat("se", value, expr)
def __int2__(self):
    from . symbolic_int import SymbolicInteger
    value = int(self.val)
    expr = ["ite", self, 1, 0]
    return SymbolicInteger("se", value, expr)

# Set the methods
SymbolicBool.__not__ = __not__
SymbolicBool.__and__ = __and__
SymbolicBool.__or__ = __or__
SymbolicBool.__xor__ = __xor__
SymbolicBool.__add__ = __add__
SymbolicBool.__bool2__ = __bool2__
SymbolicBool.__float2__ = __float2__
SymbolicBool.__int2__ = __int2__
