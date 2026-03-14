import utils

from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types.symbolic_str import SymbolicStr
from symbolic.symbolic_types.symbolic_type import SymbolicType
from z3 import *

class Z3Expression(object):
	def __init__(self):
		self.z3_vars = {}

	def toZ3(self,solver,asserts,query):
		self.z3_vars = {}
		solver.assert_exprs([self.predToZ3(p,solver) for p in asserts])
		solver.assert_exprs(Not(self.predToZ3(query,solver)))

	def predToZ3(self,pred,solver,env=None):
		sym_expr = self._astToZ3Expr(pred.symtype,solver,env)
		if env == None:
			if not is_bool(sym_expr):
				sym_expr = sym_expr != self._constant(0,solver)
			if not pred.result:
				sym_expr = Not(sym_expr)
		else:
			if not pred.result:
				sym_expr = not sym_expr
		return sym_expr

	def getIntVars(self):
		return [ v[1] for v in self.z3_vars.items() if self._isIntVar(v[1]) ]

	# ----------- private ---------------

	def _isIntVar(self, v):
		raise NotImplementedError

	def _getIntegerVariable(self,name,solver):
		if name not in self.z3_vars:
			self.z3_vars[name] = self._variable(name,solver)
		return self.z3_vars[name]

	def _variable(self,name,solver):
		raise NotImplementedError

	def _constant(self,v,solver):
		raise NotImplementedError

	def _wrapIf(self,e,solver,env):
		if env == None:
			return If(e,self._constant(1,solver),self._constant(0,solver))
		else:
			return e

	# add concrete evaluation to this, to check
	def _astToZ3Expr(self,expr,solver,env=None):
		if isinstance(expr, list):
			op = expr[0]
			args = [ self._astToZ3Expr(a,solver,env) for a in expr[1:] ]
			
			# Check if operation is unary or binary
			# Check if operation is a string operation
			if op.startswith("str."):
				# String operations can be unary or binary
				string_op = op[4:]  # Remove "str." prefix
				
				# String length operation (unary)
				if string_op == "len":
					if len(args) != 1:
						utils.crash(f"String operation {op} expects 1 argument, got {len(args)}")
					return self._str_len(args[0], solver)
				
				# String check operations (isalpha, isdigit, etc.) - unary
				elif string_op in ["isalpha", "isdigit", "islower", "isupper"]:
					if len(args) != 1:
						utils.crash(f"String operation {op} expects 1 argument, got {len(args)}")
					if string_op == "isalpha":
						return self._str_isalpha(args[0], solver)
					elif string_op == "isdigit":
						return self._str_isdigit(args[0], solver)
					elif string_op == "islower":
						return self._str_islower(args[0], solver)
					elif string_op == "isupper":
						return self._str_isupper(args[0], solver)
				
				# String transformation operations (upper, lower) - unary
				elif string_op in ["upper", "lower"]:
					if len(args) != 1:
						utils.crash(f"String operation {op} expects 1 argument, got {len(args)}")
					if string_op == "upper":
						return self._str_upper(args[0], solver)
					elif string_op == "lower":
						return self._str_lower(args[0], solver)
				
				# String comparison operations (endswith, startswith) - binary
				elif string_op in ["endswith", "startswith"]:
					if len(args) != 2:
						utils.crash(f"String operation {op} expects 2 arguments, got {len(args)}")
					if string_op == "endswith":
						return self._str_endswith(args[0], args[1], solver)
					elif string_op == "startswith":
						return self._str_startswith(args[0], args[1], solver)
				
				# String search operations (find, index) - binary or ternary
				elif string_op in ["find", "index"]:
					if len(args) < 2 or len(args) > 3:
						utils.crash(f"String operation {op} expects 2 or 3 arguments, got {len(args)}")
					if string_op == "find":
						if len(args) == 2:
							return self._str_find(args[0], args[1], solver)
						else:
							return self._str_find(args[0], args[1], solver, args[2])
					elif string_op == "index":
						if len(args) == 2:
							return self._str_index(args[0], args[1], solver)
						else:
							return self._str_index(args[0], args[1], solver, args[2])
				
				# Additional string operations for partial support
				elif string_op in ["isalnum", "isnumeric"]:
					if len(args) != 1:
						utils.crash(f"String operation {op} expects 1 argument, got {len(args)}")
					# For now, return symbolic boolean
					return self._wrapIf(self._constant(1, solver) == self._constant(1, solver), solver, env)
				
				# String strip operations
				elif string_op in ["strip", "lstrip", "rstrip"]:
					if len(args) != 1:
						utils.crash(f"String operation {op} expects 1 argument, got {len(args)}")
					if string_op == "strip":
						return self._str_strip(args[0], solver)
					elif string_op == "lstrip":
						return self._str_lstrip(args[0], solver)
					elif string_op == "rstrip":
						return self._str_rstrip(args[0], solver)
				
				# String split operation
				elif string_op == "split":
					if len(args) < 1 or len(args) > 2:
						utils.crash(f"String operation {op} expects 1 or 2 arguments, got {len(args)}")
					if len(args) == 1:
						return self._str_split(args[0], solver)
					else:
						return self._str_split(args[0], solver, args[1])
				
				# String replace operation
				elif string_op == "replace":
					if len(args) != 3:
						utils.crash(f"String operation {op} expects 3 arguments, got {len(args)}")
					return self._str_replace(args[0], args[1], args[2], solver)
				
				# Default: treat as unknown string operation
				else:
					utils.crash(f"Unsupported string operation: {op}")
			
			# Unary operations
			if op in ["abs", "neg", "pos", "trunc", "floor", "ceil", "round", "bool"]:
				if len(args) != 1:
					utils.crash(f"Unary operation {op} expects 1 argument, got {len(args)}")
				z3_arg = args[0]
				
				if op == "abs":
					return self._abs(z3_arg, solver)
				elif op == "neg":
					return self._neg(z3_arg, solver)
				elif op == "pos":
					return z3_arg  # Positive is identity
				elif op == "trunc":
					return z3_arg  # For integers, trunc is identity
				elif op == "floor":
					return z3_arg  # For integers, floor is identity
				elif op == "ceil":
					return z3_arg  # For integers, ceil is identity
				elif op == "round":
					return z3_arg  # For integers, round is identity
				elif op == "bool":
					# Convert to boolean (non-zero)
					return self._wrapIf(z3_arg != self._constant(0, solver), solver, env)
			
			# Binary operations - expect 2 arguments
			if len(args) < 2:
				utils.crash(f"Binary operation {op} expects at least 2 arguments, got {len(args)}")
			z3_l, z3_r = args[0], args[1]

			# arithmetical operations
			if op == "+":
				return self._add(z3_l, z3_r, solver)
			elif op == "-":
				return self._sub(z3_l, z3_r, solver)
			elif op == "*":
				return self._mul(z3_l, z3_r, solver)
			elif op == "//":
				return self._floordiv(z3_l, z3_r, solver)
			elif op == "%":
				return self._mod(z3_l, z3_r, solver)
			elif op == "/":
				return self._truediv(z3_l, z3_r, solver)
			elif op == "**":
				return self._pow(z3_l, z3_r, solver)

			# bitwise
			elif op == "<<":
				return self._lsh(z3_l, z3_r, solver)
			elif op == ">>":
				return self._rsh(z3_l, z3_r, solver)
			elif op == "^":
				return self._xor(z3_l, z3_r, solver)
			elif op == "|":
				return self._or(z3_l, z3_r, solver)
			elif op == "&":
				return self._and(z3_l, z3_r, solver)

			# equality gets coerced to integer
			elif op == "==":
				return self._wrapIf(z3_l == z3_r,solver,env)
			elif op == "!=":
				return self._wrapIf(z3_l != z3_r,solver,env)
			elif op == "<":
				return self._wrapIf(z3_l < z3_r,solver,env)
			elif op == ">":
				return self._wrapIf(z3_l > z3_r,solver,env)
			elif op == "<=":
				return self._wrapIf(z3_l <= z3_r,solver,env)
			elif op == ">=":
				return self._wrapIf(z3_l >= z3_r,solver,env)
			else:
				utils.crash("Unknown operation during conversion from ast to Z3 (expressions): %s" % op)

		elif isinstance(expr, SymbolicInteger):
			if expr.isVariable():
				if env == None:
					return self._getIntegerVariable(expr.name,solver)
				else:
					return env[expr.name]
			else:
				return self._astToZ3Expr(expr.expr,solver,env)

		elif isinstance(expr, SymbolicStr):
			if expr.isVariable():
				if env == None:
					# For now, treat string variables as constants with their concrete value
					# This will be improved when Z3 string support is added
					return self._string_constant(expr.getConcrValue(), solver)
				else:
					# In concrete evaluation mode, return the concrete value
					return env[expr.name] if expr.name in env else expr.getConcrValue()
			else:
				return self._astToZ3Expr(expr.expr, solver, env)

		elif isinstance(expr, SymbolicType):
			utils.crash("{} is an unsupported SymbolicType of {}".
						format(expr, type(expr)))

		elif isinstance(expr, int):
			if env == None:
				return self._constant(expr,solver)
			else:
				return expr
		
		elif isinstance(expr, str):
			if env == None:
				return self._string_constant(expr, solver)
			else:
				return expr
		
		else:
			utils.crash("Unknown node during conversion from ast to Z3 (expressions): %s" % expr)

	def _add(self, l, r, solver):
		return l + r

	def _sub(self, l, r, solver):
		return l - r

	def _mul(self, l, r, solver):
		return l * r

	def _div(self, l, r, solver):
		return l / r
	
	def _floordiv(self, l, r, solver):
		"""Integer floor division (//). Default implementation uses integer division."""
		return l / r
	
	def _truediv(self, l, r, solver):
		"""True division (/). For integers, this returns a rational number.
		Default implementation raises NotImplementedError."""
		raise NotImplementedError("_truediv not implemented")

	def _mod(self, l, r, solver):
		return l % r

	def _lsh(self, l, r, solver):
		return l << r

	def _rsh(self, l, r, solver):
		return l >> r

	def _xor(self, l, r, solver):
		return l ^ r

	def _or(self, l, r, solver):
		return l | r

	def _and(self, l, r, solver):
		return l & r
	
	def _abs(self, v, solver):
		# Default absolute value implementation - should be overridden by subclasses
		raise NotImplementedError("_abs not implemented")
	
	def _neg(self, v, solver):
		# Default negation implementation - should be overridden by subclasses
		raise NotImplementedError("_neg not implemented")
	
	def _string_constant(self, s, solver):
		"""Convert a Python string to a Z3 string constant.
		Default implementation raises NotImplementedError.
		Subclasses should override this method to provide proper string support."""
		raise NotImplementedError("String constants not supported in this Z3 expression type")
	
	# String operation methods - default implementations
	# Subclasses should override these for proper string support
	
	def _str_len(self, s, solver):
		"""String length operation - str.len"""
		raise NotImplementedError("String length operation not supported")
	
	def _str_isalpha(self, s, solver):
		"""String isalpha check - str.isalpha"""
		raise NotImplementedError("String isalpha operation not supported")
	
	def _str_isdigit(self, s, solver):
		"""String isdigit check - str.isdigit"""
		raise NotImplementedError("String isdigit operation not supported")
	
	def _str_islower(self, s, solver):
		"""String islower check - str.islower"""
		raise NotImplementedError("String islower operation not supported")
	
	def _str_isupper(self, s, solver):
		"""String isupper check - str.isupper"""
		raise NotImplementedError("String isupper operation not supported")
	
	def _str_upper(self, s, solver):
		"""String upper case conversion - str.upper"""
		raise NotImplementedError("String upper operation not supported")
	
	def _str_lower(self, s, solver):
		"""String lower case conversion - str.lower"""
		raise NotImplementedError("String lower operation not supported")
	
	def _str_endswith(self, s, suffix, solver):
		"""String endswith check - str.endswith"""
		raise NotImplementedError("String endswith operation not supported")
	
	def _str_startswith(self, s, prefix, solver):
		"""String startswith check - str.startswith"""
		raise NotImplementedError("String startswith operation not supported")
	
	def _str_find(self, s, sub, solver, beg=0):
		"""String find operation - str.find"""
		raise NotImplementedError("String find operation not supported")
	
	def _str_index(self, s, sub, solver, beg=0, end=None):
		"""String index operation - str.index"""
		raise NotImplementedError("String index operation not supported")
