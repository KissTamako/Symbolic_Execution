from z3 import Real, RealVal, ToInt, ToReal

import utils

from .expression import Z3Expression


class Z3Float(Z3Expression):
    def __init__(self, enable_simplify=False):
        super(Z3Float, self).__init__(enable_simplify)

    def _isIntVar(self, value):
        return False

    def _variable(self, name, solver):
        return Real(name, solver.ctx)

    def _constant(self, value, solver):
        if isinstance(value, float):
            return RealVal(repr(value), solver.ctx)
        return RealVal(str(value), solver.ctx)

    def _mod(self, left, right, solver):
        quotient = ToReal(ToInt(left / right))
        return left - (right * quotient)

    def _lsh(self, left, right, solver):
        utils.crash("Bitwise left shift is not supported for floating-point expressions")

    def _rsh(self, left, right, solver):
        utils.crash("Bitwise right shift is not supported for floating-point expressions")

    def _xor(self, left, right, solver):
        utils.crash("Bitwise xor is not supported for floating-point expressions")

    def _or(self, left, right, solver):
        utils.crash("Bitwise or is not supported for floating-point expressions")

    def _and(self, left, right, solver):
        utils.crash("Bitwise and is not supported for floating-point expressions")

    def getIntVars(self):
        return []
