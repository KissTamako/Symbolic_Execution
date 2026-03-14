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

	def _op_worker(self,args,fun,op):
		return self._do_sexpr(args, fun, op, SymbolicInteger.wrap)
	
	# New unary operations added for PyCT compatibility
	def __abs__(self):
		return self._op_worker([self], lambda x: abs(x), "abs")
	
	def __neg__(self):
		return self._op_worker([self], lambda x: -x, "neg")
	
	def __pos__(self):
		return self._op_worker([self], lambda x: +x, "pos")
	
	def __round__(self, ndigits=None):
		if ndigits is None:
			return self._op_worker([self], lambda x: round(x), "round")
		else:
			return self._op_worker([self, ndigits], lambda x, n: round(x, n), "round_ndigits")
	
	def __trunc__(self):
		# trunc returns integer part, same as int() for integers
		return self._op_worker([self], lambda x: int(x), "trunc")
	
	def __floor__(self):
		# For integers, floor is the same as the value itself
		return self._op_worker([self], lambda x: int(x), "floor")
	
	def __ceil__(self):
		# For integers, ceil is the same as the value itself
		return self._op_worker([self], lambda x: int(x), "ceil")
	
	# Missing methods from Python int type
	def __format__(self, format_spec=""):
		"""Format the integer according to format_spec."""
		# __format__ must return a str, not a SymbolicInteger
		# So we format the concrete value
		return format(self.val, format_spec)
	
	def __index__(self):
		"""Return the integer as an index."""
		# __index__ should return an int, not a SymbolicInteger
		return self.val
	
	def as_integer_ratio(self):
		"""Return integer ratio (self, 1)."""
		# Returns a tuple (numerator, denominator)
		# For integers, denominator is always 1
		# Note: Python's int.as_integer_ratio() returns (numerator, denominator) as ints
		# We return a tuple of SymbolicInteger objects
		return (self, SymbolicInteger("const", 1, 1))
	
	def bit_length(self):
		"""Number of bits necessary to represent self in binary."""
		return self._op_worker([self], lambda x: x.bit_length(), "bit_length")
	
	def to_bytes(self, length, byteorder='big', *, signed=False):
		"""Convert integer to bytes."""
		# This is complex for symbolic execution, so we return concrete bytes
		# For now, convert the concrete value
		# Note: The * in parameters makes 'signed' keyword-only as in Python's int.to_bytes
		concrete_bytes = self.val.to_bytes(length, byteorder, signed=signed)
		# Return as bytes (could be wrapped in SymbolicBytes if we had that type)
		return concrete_bytes
	
	# Complex number attributes (for compatibility)
	@property
	def conjugate(self):
		# For real integers, conjugate is self
		return self
	
	@property
	def denominator(self):
		# For integers, denominator is 1
		return SymbolicInteger("const", 1, 1)
	
	@property
	def imag(self):
		# For real integers, imaginary part is 0
		return SymbolicInteger("const", 0, 0)
	
	@property
	def numerator(self):
		# For integers, numerator is the integer itself
		return self
	
	@property
	def real(self):
		# For real integers, real part is self
		return self
	
	# Bool conversion is handled by SymbolicObject.__bool__
	# which returns concrete bool and records path constraint

# now update the SymbolicInteger class for operations we
# will build symbolic terms for

ops =  [("add",    "+"  ),\
	("sub",    "-"  ),\
	("mod",    "%"  ),\
	("floordiv", "//" ),\
	("truediv", "/"  ),\
	("and",    "&"  ),\
	("or",     "|"  ),\
	("xor",    "^"  ),\
	("lshift", "<<" ),\
	("rshift", ">>" ),\
	("pow",    "**" ) ]

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

# Special methods that need custom implementation
def __invert__(self):
	"""Bitwise invert operator (~)."""
	return self._op_worker([self], lambda x: ~x, "invert")

SymbolicInteger.__invert__ = __invert__

# Note: __rinvert__ doesn't exist for invert (unary operator)

def __divmod__(self, other):
	"""Return (self // other, self % other)."""
	# divmod returns a tuple of two values
	# We need to create a tuple of SymbolicIntegers
	# For now, return a concrete tuple
	quotient = self.__floordiv__(other)
	remainder = self.__mod__(other)
	return (quotient, remainder)

def __rdivmod__(self, other):
	"""Return (other // self, other % self)."""
	quotient = other.__floordiv__(self) if hasattr(other, '__floordiv__') else other // self
	remainder = other.__mod__(self) if hasattr(other, '__mod__') else other % self
	return (quotient, remainder)

SymbolicInteger.__divmod__ = __divmod__
SymbolicInteger.__rdivmod__ = __rdivmod__

