# Copyright: copyright.txt

from . symbolic_type import SymbolicObject

# we use multiple inheritance to achieve concrete execution for any
# operation for which we don't have a symbolic representation. As
# we can see a SymbolicInteger is both symbolic (SymbolicObject) and 
# concrete (int)

class SymbolicInteger(SymbolicObject,int):
	# since we are inheriting from int, we need to use new
	# to perform construction correctly
	def __new__(cls, name, v, expr=None):
		return int.__new__(cls, v)

	def __init__(self, name, v, expr=None):
		SymbolicObject.__init__(self, name, expr)
		self.val = v

	def getConcrValue(self):
		return self.val

	def wrap(conc,sym):
		return SymbolicInteger("se",conc,sym)

	def __hash__(self):
		return hash(self.val)

	def _op_worker(self,args,fun,op, wrap=None):
		if wrap is None:
			wrap = SymbolicInteger.wrap
		return self._do_sexpr(args, fun, op, wrap)

	# 一元运算
	def __abs__(self):
		"""abs(self)"""
		value = abs(self.val)
		expr = ["abs", self]
		return SymbolicInteger("se", value, expr)

	def __neg__(self):
		"""-self"""
		value = -self.val
		expr = ["-", self]
		return SymbolicInteger("se", value, expr)

	def __pos__(self):
		"""+self"""
		return self

	# 除法运算
	def __truediv__(self, other):
		"""Return self/value."""
		from . symbolic_float import SymbolicFloat
		value = self.val / other
		expr = ["/", self, other]
		return SymbolicFloat("se", value, expr)

	def __rtruediv__(self, other):
		"""Return value/self."""
		from . symbolic_float import SymbolicFloat
		value = other / self.val
		expr = ["/", other, self]
		return SymbolicFloat("se", value, expr)

	# 布尔转换 - 使用基类实现
	def __bool__(self):
		return super(SymbolicInteger, self).__bool__()

	# 辅助方法
	def __bool2__(self):
		"""Convert to symbolic bool"""
		from . symbolic_bool import SymbolicBool
		value = bool(self.val)
		expr = ["not", ["=", self, 0]]
		return SymbolicBool("se", value, expr)

	def __float2__(self):
		"""Convert to symbolic float"""
		from . symbolic_float import SymbolicFloat
		value = float(self.val)
		expr = ["to_real", self]
		return SymbolicFloat("se", value, expr)

	def __int2__(self):
		"""Convert to symbolic int"""
		return self

	def __str2__(self):
		"""Convert to symbolic string"""
		from . symbolic_str import SymbolicStr
		value = str(self.val)
		if self.val < 0:
			expr = ["str.++", "-", ["int.to.str", ["-", self]]]
		else:
			expr = ["int.to.str", self]
		return SymbolicStr("se", value, expr)

	# 其他方法
	def as_integer_ratio(self):
		"""Return integer ratio"""
		return self.val.as_integer_ratio()

	def bit_length(self):
		"""Number of bits necessary to represent self in binary"""
		return self.val.bit_length()

	def conjugate(self):
		"""Returns self, the complex conjugate of any int"""
		return self

	@property
	def denominator(self):
		"""the denominator of a rational number in lowest terms"""
		return 1

	@property
	def imag(self):
		"""the imaginary part of a complex number"""
		return 0

	@property
	def numerator(self):
		"""the numerator of a rational number in lowest terms"""
		return self

	@property
	def real(self):
		"""the real part of a complex number"""
		return self

	def to_bytes(self, length, byteorder, *, signed=False):
		"""Return an array of bytes representing an integer"""
		return self.val.to_bytes(length, byteorder, signed=signed)

# now update the SymbolicInteger class for operations we
# will build symbolic terms for

ops =  [("add",    "+"  ),\
	("sub",    "-"  ),\
	("mul",    "*"  ),\
	("mod",    "%"  ),\
	("floordiv", "//" ),\
	("and",    "&"  ),\
	("or",     "|"  ),\
	("xor",    "^"  ),\
	("lshift", "<<" ),\
	("rshift", ">>" ) ]

def make_method(method,op,a):
	code  = "def %s(self,other):\n" % method
	code += "   return self._op_worker(%s,lambda x,y : x %s y, \"%s\")" % (a,op,op)
	locals_dict = {}
	exec(code, globals(), locals_dict)
	setattr(SymbolicInteger,method,locals_dict[method])

for (name,op) in ops:
	method  = "__%s__" % name
	make_method(method,op,"[self,other]")
	rmethod  = "__r%s__" % name
	make_method(rmethod,op,"[other,self]")

