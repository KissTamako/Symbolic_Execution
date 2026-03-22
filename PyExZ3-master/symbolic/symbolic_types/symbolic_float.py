"""SymbolicFloat - 符号浮点数类型支持框架

这个模块提供浮点数类型的符号执行支持。
浮点数符号执行比整数更复杂，因为涉及实数理论和浮点精度问题。
"""

from . symbolic_type import SymbolicObject
from .symbolic_int import SymbolicInteger

class SymbolicFloat(SymbolicObject, float):
    """符号浮点数类型 - 支持浮点数的符号执行
    
    这是一个框架实现，需要进一步完善以下功能：
    1. 浮点算术运算的符号表达式
    2. 浮点数比较操作的符号支持
    3. 特殊浮点值（NaN, Inf）的处理
    4. 浮点精度和舍入模式的符号表示
    """
    
    def __new__(cls, name, v, expr=None):
        """创建新的符号浮点数实例"""
        return float.__new__(cls, v)
    
    def __init__(self, name, v, expr=None):
        """初始化符号浮点数
        
        参数:
            name: 变量名
            v: 具体浮点数值
            expr: 符号表达式（可选）
        """
        SymbolicObject.__init__(self, name, expr)
        self.val = v
    
    def getConcrValue(self):
        """获取具体值"""
        return self.val
    
    def wrap(conc, sym):
        """包装具体值和符号表达式为SymbolicFloat
        
        参数:
            conc: 具体浮点数值
            sym: 符号表达式
        
        返回:
            SymbolicFloat实例
        """
        return SymbolicFloat("se", conc, sym)
    
    def _op_worker(self, args, fun, op):
        """符号操作工作器"""
        return self._do_sexpr(args, fun, op, SymbolicFloat.wrap)
    
    # 浮点数特有方法
    
    def __abs__(self):
        """绝对值 - 需要符号支持"""
        return self._op_worker([self], lambda x: abs(x), "abs")
    
    def __neg__(self):
        """取负 - 需要符号支持"""
        return self._op_worker([self], lambda x: -x, "neg")
    
    def __pos__(self):
        """取正 - 需要符号支持"""
        return self._op_worker([self], lambda x: +x, "pos")
    
    def __round__(self, ndigits=None):
        """四舍五入 - 需要符号支持"""
        if ndigits is None:
            return self._op_worker([self], lambda x: round(x), "round")
        else:
            return self._op_worker([self, ndigits], lambda x, n: round(x, n), "round_ndigits")
    
    def __trunc__(self):
        """截断取整 - 需要符号支持"""
        return self._op_worker([self], lambda x: int(x), "trunc")
    
    def __floor__(self):
        """向下取整 - 需要符号支持"""
        return self._op_worker([self], lambda x: int(x), "floor")
    
    def __ceil__(self):
        """向上取整 - 需要符号支持"""
        return self._op_worker([self], lambda x: int(x), "ceil")
    
    # 数学运算方法
    
    def is_integer(self):
        """检查是否为整数 - 需要符号支持"""
        return self._do_sexpr([self], lambda x: x.is_integer(), "float.is_integer", SymbolicInteger.wrap)
    
    def as_integer_ratio(self):
        """返回最简分数表示 - 需要符号支持"""
        # 返回（分子，分母）元组
        return self._do_sexpr([self], lambda x: x.as_integer_ratio(), "float.as_integer_ratio", None)
    
    def hex(self):
        """十六进制表示 - 需要符号支持"""
        return self._do_sexpr([self], lambda x: x.hex(), "float.hex", None)
    
    # 浮点数属性
    
    @property
    def imag(self):
        """虚部 - 浮点数为0"""
        return SymbolicFloat("const", 0.0, 0.0)
    
    @property
    def real(self):
        """实部 - 浮点数为其自身"""
        return self
    
    @property
    def conjugate(self):
        """共轭复数 - 浮点数为其自身"""
        return self
    
    # 特殊浮点值检查
    
    def is_nan(self):
        """检查是否为NaN - 需要符号支持"""
        return self._do_sexpr([self], lambda x: x != x, "float.is_nan", SymbolicInteger.wrap)
    
    def is_infinite(self):
        """检查是否为无穷大 - 需要符号支持"""
        import math
        return self._do_sexpr([self], lambda x: math.isinf(x), "float.is_infinite", SymbolicInteger.wrap)
    
    def is_finite(self):
        """检查是否为有限数 - 需要符号支持"""
        import math
        return self._do_sexpr([self], lambda x: math.isfinite(x), "float.is_finite", SymbolicInteger.wrap)

# 浮点数运算支持
float_ops = [
    ("add", "+"),
    ("sub", "-"),
    ("mul", "*"),
    ("truediv", "/"),
    ("mod", "%"),
    ("pow", "**")
]

def make_float_method(method, op, a):
    code = "def %s(self, other):\n" % method
    code += "    return self._op_worker(%s, lambda x, y: x %s y, \"%s\")" % (a, op, op)
    locals_dict = {}
    exec(code, globals(), locals_dict)
    setattr(SymbolicFloat, method, locals_dict[method])

for (name, op) in float_ops:
    method = "__%s__" % name
    make_float_method(method, op, "[self, other]")
    rmethod = "__r%s__" % name
    make_float_method(rmethod, op, "[other, self]")

# 内置构造函数符号化支持
@classmethod
def from_symbolic(cls, value):
    """
    符号版本的float()构造函数
    
    根据PyCT论文：float(x) → SymbolicFloat("float", x, ["float", x.expr])
    
    参数：
    value: 要转换的值，可以是具体值或符号对象
    
    返回：
    SymbolicFloat对象
    """
    if hasattr(value, 'getConcrValue'):
        # 如果value已经是符号类型，保持符号信息
        concrete_value = value.getConcrValue()
        
        # 创建符号表达式：["float", value.expr] 或 ["float", value]如果value是变量
        if value.isVariable():
            symbolic_expr = ["float", value]
        else:
            symbolic_expr = ["float", value.expr]
        
        # 创建新的SymbolicFloat对象
        return cls("float", float(concrete_value), symbolic_expr)
    else:
        # 如果value是具体值，创建普通符号对象
        return cls("float", float(value), ["float", value])

SymbolicFloat.from_symbolic = from_symbolic
