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

    def __str2__(self):
        """Convert to symbolic string"""
        from . symbolic_str import SymbolicStr
        value = str(self.val)
        expr = ["real.to.str", self]
        return SymbolicStr("se", value, expr)

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

    def __floor__(self):
        """Return the largest integer not greater than self"""
        from . symbolic_int import SymbolicInteger
        value = int(self.val // 1)
        if self.val < 0 and self.val % 1 != 0:
            value -= 1
        expr = ["floor", self]
        return SymbolicInteger("se", value, expr)

    def __ceil__(self):
        """Return the smallest integer not less than self"""
        from . symbolic_int import SymbolicInteger
        value = int(self.val // 1)
        if self.val > 0 and self.val % 1 != 0:
            value += 1
        expr = ["ceil", self]
        return SymbolicInteger("se", value, expr)

    def __complex__(self):
        """Convert to complex"""
        return complex(self.val)

    def __str__(self):
        """Convert to string"""
        return str(self.val)

    def __repr__(self):
        """Return a string representation of the object"""
        return f"SymbolicFloat({self.val}, {self.expr})"

    # 添加强制类型转换方法
    def __index__(self):
        """Called to implement operator.index() and when converting to an integer"""
        return int(self.val)

    # 添加数学辅助方法
    def __sizeof__(self):
        """Returns the size of the float object in bytes"""
        return self.val.__sizeof__()

    # 添加反向比较方法
    def __rlt__(self, other):
        """Return other < self"""
        return self._op_worker([other, self], lambda x, y: x < y, '<', SymbolicFloat.wrap)

    def __rle__(self, other):
        """Return other <= self"""
        return self._op_worker([other, self], lambda x, y: x <= y, '<=', SymbolicFloat.wrap)

    def __rgt__(self, other):
        """Return other > self"""
        return self._op_worker([other, self], lambda x, y: x > y, '>', SymbolicFloat.wrap)

    def __rge__(self, other):
        """Return other >= self"""
        return self._op_worker([other, self], lambda x, y: x >= y, '>=', SymbolicFloat.wrap)

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
    if op == '/':
        code = f"def __{method}__(self, other):\n"
        code += f"    try:\n"
        code += f"        return self._op_worker([self, other], lambda x, y: x {op} y, '{op}', SymbolicFloat.wrap)\n"
        code += f"    except ZeroDivisionError as e:\n"
        code += f"        # 处理除零错误\n"
        code += f"        raise"
    elif op == '**':
        code = f"def __{method}__(self, other):\n"
        code += f"    try:\n"
        code += f"        return self._op_worker([self, other], lambda x, y: x {op} y, '{op}', SymbolicFloat.wrap)\n"
        code += f"    except (ValueError, TypeError) as e:\n"
        code += f"        # 处理无效输入的情况\n"
        code += f"        raise"
    else:
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