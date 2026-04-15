from . symbolic_type import SymbolicObject

class SymbolicFloat(SymbolicObject):

    def __init__(self, name, v, expr=None):
        SymbolicObject.__init__(self, name, expr)
        self.val = float(v)

    def getConcrValue(self):
        return self.val

    def wrap(conc, sym):
        return SymbolicFloat("se", conc, sym)

    def __hash__(self):
        return hash(self.val)

    def _op_worker(self, args, fun, op, wrap=None):
        if wrap is None:
            wrap = SymbolicFloat.wrap
        return self._do_sexpr(args, fun, op, wrap)

    def __float__(self):
        return self.getConcrValue()

    # 一元运算
    def __abs__(self):
        """abs(self)"""
        value = abs(self.val)
        expr = ["abs", self]
        return SymbolicFloat("se", value, expr)

    def __neg__(self):
        """-self"""
        value = -self.val
        expr = ["-", self]
        return SymbolicFloat("se", value, expr)

    def __pos__(self):
        """+self"""
        return self

    # 布尔转换 - 使用基类实现
    def __bool__(self):
        return super(SymbolicFloat, self).__bool__()

    # 辅助方法

    def __bool2__(self):
        """Convert to symbolic bool"""
        from . symbolic_bool import SymbolicBool
        value = bool(self.val)
        expr = ["not", ["=", self, 0.0]]
        return SymbolicBool("se", value, expr)

    def __float2__(self):
        """Convert to symbolic float"""
        return self

    def __int2__(self):
        """Convert to symbolic int"""
        from . symbolic_int import SymbolicInteger
        value = int(self.val)
        # 处理负数的情况，因为SMT中的to_int和Python的int行为不同
        expr = ["+", ["to_int", self], ["ite", ["and", ["<", self, 0], ["not", ["is_int", self]]], 1, 0]]
        return SymbolicInteger("se", value, expr)

    # 其他方法
    def as_integer_ratio(self):
        """Return integer ratio"""
        return self.val.as_integer_ratio()

    def conjugate(self):
        """Returns self, the complex conjugate of any float"""
        return self

    def hex(self):
        """Return a hexadecimal representation of a floating-point number"""
        return self.val.hex()

    def is_integer(self):
        """Return True if the float is an integer"""
        return self.val.is_integer()

    @property
    def imag(self):
        """the imaginary part of a complex number"""
        return 0.0

    @property
    def real(self):
        """the real part of a complex number"""
        return self

    def __round__(self, n=None):
        """Return the rounded value"""
        if n is None:
            from . symbolic_int import SymbolicInteger
            value = round(self.val)
            return SymbolicInteger("se", value)
        else:
            value = round(self.val, n)
            return SymbolicFloat("se", value)

    def __trunc__(self):
        """Return the truncated value"""
        from . symbolic_int import SymbolicInteger
        value = int(self.val)
        return SymbolicInteger("se", value)

# Float operations
ops = ["add", "sub", "mul", "truediv", "mod", "pow"]

op_map = {
    "add": "+",
    "sub": "-",
    "mul": "*",
    "truediv": "/",
    "mod": "%",
    "pow": "**"
}

def make_method(method, op):
    code = f"def __{method}__(self, other):\n"
    code += f"    return self._op_worker([self, other], lambda x, y: x {op} y, '{op}', SymbolicFloat.wrap)"
    locals_dict = {}
    exec(code, globals(), locals_dict)
    setattr(SymbolicFloat, f"__{method}__", locals_dict[f"__{method}__"])

for op_name, op_symbol in op_map.items():
    make_method(op_name, op_symbol)
    make_method(f"r{op_name}", op_symbol)

# Comparison operations
comp_ops = ["lt", "le", "eq", "ne", "gt", "ge"]

comp_map = {
    "lt": "<",
    "le": "<=",
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "ge": ">="
}

for op_name, op_symbol in comp_map.items():
    make_method(op_name, op_symbol)