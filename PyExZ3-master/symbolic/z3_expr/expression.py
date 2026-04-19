import math

import utils
from symbolic.symbolic_types.symbolic_bool import SymbolicBool
from symbolic.symbolic_types.symbolic_float import SymbolicFloat
from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types.symbolic_str import SymbolicStr
from symbolic.symbolic_types.symbolic_type import SymbolicType
from z3 import *


class Z3Expression(object):
    def __init__(self, enable_simplify=False):
        self.z3_vars = {}
        self.enable_simplify = enable_simplify

    def toZ3(self, solver, asserts, query):
        self.z3_vars = {}
        assert_exprs = [self.predToZ3(predicate, solver) for predicate in asserts]
        query_expr = Not(self.predToZ3(query, solver))

        if self.enable_simplify:
            assert_exprs = [simplify(expr) for expr in assert_exprs]
            query_expr = simplify(query_expr)

        solver.assert_exprs(assert_exprs)
        solver.assert_exprs(query_expr)

    def predToZ3(self, pred, solver, env=None):
        sym_expr = self._astToZ3Expr(pred.symtype, solver, env)
        if env is None:
            sym_expr = self._coerce_to_bool(sym_expr, solver)
            if not pred.result:
                sym_expr = Not(sym_expr)
        else:
            if not pred.result:
                sym_expr = not sym_expr
        return sym_expr

    def getIntVars(self):
        return [entry[1] for entry in self.z3_vars.items() if self._isIntVar(entry[1])]

    def _isIntVar(self, value):
        raise NotImplementedException

    def _getIntegerVariable(self, name, solver):
        if name not in self.z3_vars:
            self.z3_vars[name] = self._variable(name, solver)
        return self.z3_vars[name]

    def _getStringVariable(self, name):
        if name not in self.z3_vars:
            self.z3_vars[name] = String(name)
        return self.z3_vars[name]

    def _variable(self, name, solver):
        raise NotImplementedException

    def _constant(self, value, solver):
        raise NotImplementedException

    def _coerce_to_bool(self, expr, solver):
        if is_bool(expr):
            return expr
        try:
            if expr.sort().kind() == Z3_SEQ_SORT:
                return Length(expr) != 0
        except Exception:
            pass
        return expr != self._constant(0, solver)

    def _wrapIf(self, expr, solver, env):
        if env is None:
            return If(expr, self._constant(1, solver), self._constant(0, solver))
        return expr

    def _astToZ3Expr(self, expr, solver, env=None):
        if isinstance(expr, list):
            op = expr[0]
            args = [self._astToZ3Expr(arg, solver, env) for arg in expr[1:]]

            if op == "abs":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for abs operation, got %d" % len(args))
                return If(args[0] >= 0, args[0], -args[0]) if env is None else abs(args[0])

            if op == "not":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for not operation, got %d" % len(args))
                return Not(self._coerce_to_bool(args[0], solver)) if env is None else (not args[0])

            if op == "str.len":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for str.len operation, got %d" % len(args))
                return Length(args[0]) if env is None else len(args[0])

            if op == "str.++":
                if len(args) < 2:
                    utils.crash("Expected at least 2 arguments for str.++ operation, got %d" % len(args))
                return Concat(*args) if env is None else "".join(args)

            if op == "getitem":
                if len(args) != 2:
                    utils.crash("Expected 2 arguments for getitem operation, got %d" % len(args))
                return SubString(args[0], args[1], 1) if env is None else args[0][args[1]]

            if op == "slice":
                if len(args) != 3:
                    utils.crash("Expected 3 arguments for slice operation, got %d" % len(args))
                if env is None:
                    return SubString(args[0], args[1], args[2] - args[1])
                return args[0][args[1] : args[2]]

            if op == "str.find":
                if len(args) != 3:
                    utils.crash("Expected 3 arguments for str.find operation, got %d" % len(args))
                return IndexOf(args[0], args[1], args[2]) if env is None else args[0].find(args[1], args[2])

            if op == "str.startswith":
                if len(args) != 2:
                    utils.crash(
                        "Expected 2 arguments for str.startswith operation, got %d" % len(args)
                    )
                return self._wrapIf(PrefixOf(args[1], args[0]), solver, env)

            if op == "str.endswith":
                if len(args) != 2:
                    utils.crash(
                        "Expected 2 arguments for str.endswith operation, got %d" % len(args)
                    )
                return self._wrapIf(SuffixOf(args[1], args[0]), solver, env)

            if op == "str.replace":
                if len(args) != 3:
                    utils.crash("Expected 3 arguments for str.replace operation, got %d" % len(args))
                if env is None:
                    return Replace(args[0], args[1], args[2])
                return args[0].replace(args[1], args[2], 1)

            if op == "in":
                if len(args) != 2:
                    utils.crash("Expected 2 arguments for in operation, got %d" % len(args))
                return self._wrapIf(Contains(args[0], args[1]), solver, env)

            if op == "int.to.str":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for int.to.str operation, got %d" % len(args))
                return IntToStr(args[0]) if env is None else str(args[0])

            if op == "real.to.str":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for real.to.str operation, got %d" % len(args))
                if env is None:
                    return IntToStr(ToInt(args[0]))
                return str(args[0])

            if op == "floor":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for floor operation, got %d" % len(args))
                return args[0] - (args[0] % 1) if env is None else int(args[0])

            if op == "sin":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for sin operation, got %d" % len(args))
                return args[0] if env is None else math.sin(args[0])

            if op == "cos":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for cos operation, got %d" % len(args))
                return args[0] if env is None else math.cos(args[0])

            if op == "tan":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for tan operation, got %d" % len(args))
                return args[0] if env is None else math.tan(args[0])

            if op == "asin":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for asin operation, got %d" % len(args))
                return args[0] if env is None else math.asin(args[0])

            if op == "acos":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for acos operation, got %d" % len(args))
                return args[0] if env is None else math.acos(args[0])

            if op == "atan":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for atan operation, got %d" % len(args))
                return args[0] if env is None else math.atan(args[0])

            if op == "sqrt":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for sqrt operation, got %d" % len(args))
                return args[0] if env is None else math.sqrt(args[0])

            if op == "exp":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for exp operation, got %d" % len(args))
                return args[0] if env is None else math.exp(args[0])

            if op == "log":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for log operation, got %d" % len(args))
                return args[0] if env is None else math.log(args[0])

            if op == "log10":
                if len(args) != 1:
                    utils.crash("Expected 1 argument for log10 operation, got %d" % len(args))
                return args[0] if env is None else math.log10(args[0])

            if len(args) != 2:
                utils.crash("Expected 2 arguments for binary operation, got %d" % len(args))

            left, right = args[0], args[1]

            if op == "+":
                return self._add(left, right, solver)
            if op == "-":
                return self._sub(left, right, solver)
            if op == "*":
                return self._mul(left, right, solver)
            if op in {"//", "/"}:
                return self._div(left, right, solver)
            if op == "%":
                return self._mod(left, right, solver)

            if op == "<<":
                return self._lsh(left, right, solver)
            if op == ">>":
                return self._rsh(left, right, solver)
            if op == "^":
                return self._xor(left, right, solver)
            if op == "|":
                return self._or(left, right, solver)
            if op == "&":
                return self._and(left, right, solver)

            if op in {"==", "="}:
                return self._wrapIf(left == right, solver, env)
            if op == "!=":
                return self._wrapIf(left != right, solver, env)
            if op == "<":
                return self._wrapIf(left < right, solver, env)
            if op == ">":
                return self._wrapIf(left > right, solver, env)
            if op == "<=":
                return self._wrapIf(left <= right, solver, env)
            if op == ">=":
                return self._wrapIf(left >= right, solver, env)

            utils.crash("Unknown BinOp during conversion from ast to Z3 (expressions): %s" % op)

        if isinstance(expr, SymbolicInteger):
            if expr.isVariable():
                return self._getIntegerVariable(expr.name, solver) if env is None else env[expr.name]
            return self._astToZ3Expr(expr.expr, solver, env)

        if isinstance(expr, SymbolicBool):
            if expr.isVariable():
                return self._getIntegerVariable(expr.name, solver) if env is None else env[expr.name]
            return self._astToZ3Expr(expr.expr, solver, env)

        if isinstance(expr, SymbolicFloat):
            if expr.isVariable():
                return self._getIntegerVariable(expr.name, solver) if env is None else env[expr.name]
            return self._astToZ3Expr(expr.expr, solver, env)

        if isinstance(expr, SymbolicStr):
            if expr.isVariable():
                return self._getStringVariable(expr.name) if env is None else env[expr.name]
            return self._astToZ3Expr(expr.expr, solver, env)

        if isinstance(expr, SymbolicType):
            utils.crash("{} is an unsupported SymbolicType of {}".format(expr, type(expr)))

        if isinstance(expr, int):
            return self._constant(expr, solver) if env is None else expr

        if isinstance(expr, str):
            return StringVal(expr) if env is None else expr

        utils.crash("Unknown node during conversion from ast to Z3 (expressions): %s" % expr)

    def _add(self, left, right, solver):
        return left + right

    def _sub(self, left, right, solver):
        return left - right

    def _mul(self, left, right, solver):
        return left * right

    def _div(self, left, right, solver):
        return left / right

    def _mod(self, left, right, solver):
        return left % right

    def _lsh(self, left, right, solver):
        return left << right

    def _rsh(self, left, right, solver):
        return left >> right

    def _xor(self, left, right, solver):
        return left ^ right

    def _or(self, left, right, solver):
        return left | right

    def _and(self, left, right, solver):
        return left & right
