import utils

from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types.symbolic_str import SymbolicStr
from symbolic.symbolic_types.symbolic_type import SymbolicType
from symbolic.symbolic_types.symbolic_float import SymbolicFloat
from symbolic.symbolic_types.symbolic_range import SymbolicRange
from symbolic.symbolic_types.symbolic_list import SymbolicList
from symbolic.symbolic_types.symbolic_dict import SymbolicDict
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
		# 如果expr已经是Z3表达式，直接返回
		from z3 import ExprRef
		if isinstance(expr, ExprRef):
			return expr
		
		if isinstance(expr, list):
			# 首先检查是否是具体的Python列表（不是符号表达式）
			if len(expr) == 0 or not isinstance(expr[0], str):
				# 这是一个具体的Python列表（不是符号表达式）
				# 例如：[1, 2, 3] 而不是 ["+", x, y]
				return self._list_constant(expr, solver)
			
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
			
			# Range operations
			if op.startswith("range."):
				range_op = op[6:]  # Remove "range." prefix
				
				# Range length operation
				if range_op == "len":
					if len(args) != 1:
						utils.crash(f"Range operation {op} expects 1 argument, got {len(args)}")
					return self._range_len(args[0], solver)
				
				# Range comparison operations
				elif range_op in ["eq", "ne", "lt", "le", "gt", "ge"]:
					if len(args) != 2:
						utils.crash(f"Range operation {op} expects 2 arguments, got {len(args)}")
					z3_l, z3_r = args[0], args[1]
					
					if range_op == "eq":
						return self._wrapIf(z3_l == z3_r, solver, env)
					elif range_op == "ne":
						return self._wrapIf(z3_l != z3_r, solver, env)
					elif range_op == "lt":
						return self._wrapIf(z3_l < z3_r, solver, env)
					elif range_op == "le":
						return self._wrapIf(z3_l <= z3_r, solver, env)
					elif range_op == "gt":
						return self._wrapIf(z3_l > z3_r, solver, env)
					elif range_op == "ge":
						return self._wrapIf(z3_l >= z3_r, solver, env)
				
				# Range contains operation
				elif range_op == "contains":
					if len(args) != 2:
						utils.crash(f"Range operation {op} expects 2 arguments, got {len(args)}")
					return self._range_contains(args[0], args[1], solver)
				
				# Range count operation
				elif range_op == "count":
					if len(args) != 2:
						utils.crash(f"Range operation {op} expects 2 arguments, got {len(args)}")
					return self._range_count(args[0], args[1], solver)
				
				# Range index operation
				elif range_op == "index":
					if len(args) != 2:
						utils.crash(f"Range operation {op} expects 2 arguments, got {len(args)}")
					return self._range_index(args[0], args[1], solver)
				
				# Range getitem operation
				elif range_op == "getitem":
					if len(args) != 2:
						utils.crash(f"Range operation {op} expects 2 arguments, got {len(args)}")
					return self._range_getitem(args[0], args[1], solver)
				
				# Default: treat as unknown range operation
				else:
					utils.crash(f"Unsupported range operation: {op}")
			
			# Range constructor
			elif op == "range":
				if len(args) < 1 or len(args) > 3:
					utils.crash(f"Range constructor expects 1-3 arguments, got {len(args)}")
				
				if len(args) == 1:
					# range(stop) format
					stop = args[0]
					start = self._constant(0, solver)
					step = self._constant(1, solver)
				elif len(args) == 2:
					# range(start, stop) format
					start, stop = args[0], args[1]
					step = self._constant(1, solver)
				else:
					# range(start, stop, step) format
					start, stop, step = args[0], args[1], args[2]
				
				# For now, return the start value as a placeholder
				# In full implementation, this would create a Z3 sequence
				return start
			
			# Range constant
			elif op == "range_const":
				if len(args) != 3:
					utils.crash(f"Range constant expects 3 arguments (start, stop, step), got {len(args)}")
				
				# For now, return the start value
				return args[0]
			
			# Range element
			elif op == "range_elem":
				# range_elem expression: ["range_elem", start, step?, index?]
				# Accept 3 or 4 arguments for backward compatibility
				if len(args) != 3 and len(args) != 4:
					utils.crash(f"Range element expects 3 or 4 arguments, got {len(args)}")
				
				# start + step * index
				if len(args) == 3:
					# args: start, step, index
					start, step, index = args[0], args[1], args[2]
				else:
					# args: start, stop?, step?, index? - use start, step, index (args[3])
					start, step, index = args[0], args[1], args[3]
				return start + (step * index)
			
			# Range slice
			elif op == "range_slice":
				if len(args) != 7:
					utils.crash(f"Range slice expects 7 arguments, got {len(args)}")
				
				# For now, return the original start
				return args[0]
			
			# Range reversed
			elif op == "range.reversed":
				if len(args) != 4:
					utils.crash(f"Range reversed expects 4 arguments, got {len(args)}")
				
				# For now, return the original start
				return args[0]
			
			# Built-in constructors (int, float, str, range, list, dict, bool)
			if op in ["int", "float", "str", "range", "list", "dict", "bool"]:
				# For now, just return the first argument
				# These constructors should preserve symbolic information
				# In proper implementation, we would create a new symbolic expression
				if len(args) == 1:
					return args[0]
				elif len(args) == 2 and op == "int":
					# int(x, base) format - for now just return x
					return args[0]
				else:
					# For now, return the first argument
					return args[0] if args else self._constant(0, solver)
			
			# List operations
			if op.startswith("list."):
				list_op = op[5:]  # Remove "list." prefix
				
				# List length operation
				if list_op == "len":
					if len(args) != 1:
						utils.crash(f"List operation {op} expects 1 argument, got {len(args)}")
					return self._list_len(args[0], solver)
				
				# List getitem operation
				elif list_op == "getitem":
					if len(args) != 2:
						utils.crash(f"List operation {op} expects 2 arguments, got {len(args)}")
					return self._list_getitem(args[0], args[1], solver)
				
				# List contains operation
				elif list_op == "contains":
					if len(args) != 2:
						utils.crash(f"List operation {op} expects 2 arguments, got {len(args)}")
					return self._list_contains(args[0], args[1], solver)
				
				# List count operation
				elif list_op == "count":
					if len(args) != 2:
						utils.crash(f"List operation {op} expects 2 arguments, got {len(args)}")
					return self._list_count(args[0], args[1], solver)
				
				# List index operation
				elif list_op == "index":
					if len(args) >= 2 and len(args) <= 4:
						# args: list, value, start, end
						return self._list_index(args[0], args[1], solver, 
											   args[2] if len(args) > 2 else 0,
											   args[3] if len(args) > 3 else None)
					else:
						utils.crash(f"List operation {op} expects 2-4 arguments, got {len(args)}")
				
				# List constructor
				elif list_op == "constructor":
					# Create a list from elements
					return self._list_constructor(args, solver)
				
				# Default: treat as unknown list operation
				else:
					utils.crash(f"Unsupported list operation: {op}")
			
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
			elif op == "slice":
				# Slice operation: slice(sequence, start, stop, step)
				# For now, return the original sequence as a placeholder
				# In proper implementation, this would extract a slice
				if len(args) >= 1:
					return args[0]  # Return the original sequence
				else:
					utils.crash(f"Slice operation expects at least 1 argument, got {len(args)}")
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

		elif isinstance(expr, SymbolicFloat):
			# SymbolicFloat support - implement proper Z3 Real variable/constant support
			if expr.isVariable():
				if env == None:
					# Create Z3 Real variable for symbolic float
					# Check if _getFloatVariable method exists (implemented in subclasses)
					if hasattr(self, '_getFloatVariable'):
						return self._getFloatVariable(expr.name, solver)
					else:
						# Fallback: return concrete float value as Real constant
						return self._float_constant(expr.getConcrValue(), solver)
				else:
					return env.get(expr.name, expr.getConcrValue())
			else:
				return self._astToZ3Expr(expr.expr, solver, env)

		elif isinstance(expr, SymbolicRange):
			# SymbolicRange support - implement proper Z3 Seq/range support
			if expr.isVariable():
				if env == None:
					# Create Z3 representation for symbolic range
					# Check if _getRangeVariable method exists (implemented in subclasses)
					if hasattr(self, '_getRangeVariable'):
						return self._getRangeVariable(expr.name, solver)
					else:
						# Fallback: return concrete range value
						return self._range_constant(expr.getConcrValue(), solver)
				else:
					return env.get(expr.name, expr.getConcrValue())
			else:
				return self._astToZ3Expr(expr.expr, solver, env)

		elif isinstance(expr, SymbolicList):
			# SymbolicList support - implement proper Z3 Array/list support
			if expr.isVariable():
				if env == None:
					# Create Z3 Array variable for symbolic list
					# Check if _getListVariable method exists (implemented in subclasses)
					if hasattr(self, '_getListVariable'):
						return self._getListVariable(expr.name, solver)
					else:
						# Fallback: return concrete list value as Array constant
						return self._list_constant(expr.getConcrValue(), solver)
				else:
					return env.get(expr.name, expr.getConcrValue())
			else:
				return self._astToZ3Expr(expr.expr, solver, env)

		elif isinstance(expr, SymbolicDict):
			# SymbolicDict support - implement proper Z3 Map/dict support
			if expr.isVariable():
				if env == None:
					# Create Z3 Array variable for symbolic dict
					# Check if _getDictVariable method exists (implemented in subclasses)
					if hasattr(self, '_getDictVariable'):
						return self._getDictVariable(expr.name, solver)
					else:
						# Fallback: return concrete dict value as Array constant
						return self._dict_constant(expr.getConcrValue(), solver)
				else:
					return env.get(expr.name, expr.getConcrValue())
			else:
				return self._astToZ3Expr(expr.expr, solver, env)

		elif isinstance(expr, SymbolicType):
			# This should only be reached for truly unknown SymbolicType subclasses
			utils.crash("{} is an unsupported SymbolicType of {}".
						format(expr, type(expr)))

		# Python built-in types (must come after symbolic types to avoid misclassification)
		elif isinstance(expr, int):
			if env == None:
				return self._constant(expr,solver)
			else:
				return expr
		
		elif isinstance(expr, float):
			if env == None:
				return self._float_constant(expr, solver)
			else:
				return expr
		
		elif isinstance(expr, str):
			if env == None:
				return self._string_constant(expr, solver)
			else:
				return expr
		
		elif isinstance(expr, range):
			if env == None:
				return self._range_constant(expr, solver)
			else:
				return expr
		
		elif isinstance(expr, dict):
			if env == None:
				return self._dict_constant(expr, solver)
			else:
				return expr
		
		elif isinstance(expr, list) and not isinstance(expr, SymbolicList):
			# Check if this is a symbolic list expression (list of op + args)
			# Not to be confused with SymbolicList instances (handled above)
			if len(expr) > 0 and isinstance(expr[0], str):
				op = expr[0]
				args = [ self._astToZ3Expr(a,solver,env) for a in expr[1:] ]
				
				# Handle list operations
				if op.startswith("list."):
					list_op = op[5:]  # Remove "list." prefix
					
					# List length operation
					if list_op == "len":
						if len(args) != 1:
							utils.crash(f"List operation {op} expects 1 argument, got {len(args)}")
						return self._list_len(args[0], solver)
					
					# List getitem operation
					elif list_op == "getitem":
						if len(args) != 2:
							utils.crash(f"List operation {op} expects 2 arguments, got {len(args)}")
						return self._list_getitem(args[0], args[1], solver)
					
					# List contains operation
					elif list_op == "contains":
						if len(args) != 2:
							utils.crash(f"List operation {op} expects 2 arguments, got {len(args)}")
						return self._list_contains(args[0], args[1], solver)
					
					# List count operation
					elif list_op == "count":
						if len(args) != 2:
							utils.crash(f"List operation {op} expects 2 arguments, got {len(args)}")
						return self._list_count(args[0], args[1], solver)
					
					# List index operation
					elif list_op == "index":
						if len(args) >= 2 and len(args) <= 4:
							# args: list, value, start, end
							return self._list_index(args[0], args[1], solver, 
												   args[2] if len(args) > 2 else 0,
												   args[3] if len(args) > 3 else None)
						else:
							utils.crash(f"List operation {op} expects 2-4 arguments, got {len(args)}")
					
					# List constructor
					elif list_op == "constructor":
						# Create a list from elements
						return self._list_constructor(args, solver)
					
					# Default: treat as unknown list operation
					else:
						utils.crash(f"Unsupported list operation: {op}")
				
				# Handle other list expressions (like ["+", x, y] which are already handled above)
				# This case shouldn't be reached because all operations are handled above
				else:
					utils.crash(f"Unexpected list expression with op {op}")
			else:
				# This is a concrete Python list (not a symbolic expression)
				# For now, return a constant 0
				# In full implementation, we would convert to Z3 array constant
				return self._list_constant(expr, solver)
		
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
	
	def _float_constant(self, v, solver):
		"""Convert a Python float to a Z3 Real constant.
		Default implementation raises NotImplementedError.
		Subclasses should override this method to provide proper float support."""
		raise NotImplementedError("Float constants not supported in this Z3 expression type")
	
	def _range_constant(self, v, solver):
		"""Convert a Python range to a Z3 Seq constant.
		Default implementation raises NotImplementedError.
		Subclasses should override this method to provide proper range support."""
		raise NotImplementedError("Range constants not supported in this Z3 expression type")
	
	def _list_constant(self, v, solver):
		"""Convert a Python list to a Z3 Array constant.
		Default implementation raises NotImplementedError.
		Subclasses should override this method to provide proper list support."""
		raise NotImplementedError("List constants not supported in this Z3 expression type")
	
	def _dict_constant(self, v, solver):
		"""Convert a Python dict to a Z3 Map constant.
		Default implementation raises NotImplementedError.
		Subclasses should override this method to provide proper dict support."""
		raise NotImplementedError("Dict constants not supported in this Z3 expression type")
	
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
	
	# List operation methods - default implementations
	# Subclasses should override these for proper list support
	
	def _list_len(self, l, solver):
		"""List length operation - list.len"""
		raise NotImplementedError("List length operation not supported")
	
	def _list_getitem(self, l, index, solver):
		"""List getitem operation - list.getitem"""
		raise NotImplementedError("List getitem operation not supported")
	
	def _list_contains(self, l, item, solver):
		"""List contains operation - list.contains"""
		raise NotImplementedError("List contains operation not supported")
	
	def _list_count(self, l, item, solver):
		"""List count operation - list.count"""
		raise NotImplementedError("List count operation not supported")
	
	def _list_index(self, l, item, solver, start=0, end=None):
		"""List index operation - list.index"""
		raise NotImplementedError("List index operation not supported")
	
	def _list_constructor(self, elements, solver):
		"""List constructor - create a list from elements"""
		raise NotImplementedError("List constructor not supported")
