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
		# Filter out None assertions
		valid_asserts = [p for p in asserts if p is not None]
		solver.assert_exprs([self.predToZ3(p,solver) for p in valid_asserts])
		if query is not None:
			solver.assert_exprs(Not(self.predToZ3(query,solver)))

	def predToZ3(self,pred,solver,env=None):
		sym_expr = self._astToZ3Expr(pred.symtype,solver,env)
		if env == None:
			if not is_bool(sym_expr):
				sym_expr = sym_expr != self._constant(0,solver)
			if not pred.result:
				sym_expr = Not(sym_expr)
		else:
			# When env is provided, we're evaluating concretely
			# sym_expr should be a concrete Python value (bool, int, etc.)
			# For predicate evaluation, we need to convert to bool
			if not isinstance(sym_expr, bool):
				# Convert non-bool to bool (e.g., int != 0)
				sym_expr = bool(sym_expr)
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
			z3_l,z3_r = args[0],args[1]

			# arithmetical operations
			if op == "+":
				return self._add(z3_l, z3_r, solver)
			elif op == "-":
				return self._sub(z3_l, z3_r, solver)
			elif op == "*":
				return self._mul(z3_l, z3_r, solver)
			elif op == "//":
				return self._div(z3_l, z3_r, solver)
			elif op == "%":
				return self._mod(z3_l, z3_r, solver)

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
				utils.crash("Unknown BinOp during conversion from ast to Z3 (expressions): %s" % op)

		elif isinstance(expr, SymbolicInteger):
			if expr.isVariable():
				if env == None:
					# Handle 'const' variable specially - it's not a real variable
					if expr.name == 'const':
						# 'const' is a placeholder for concrete constants
						# Return concrete value as Z3 constant
						concrete_val = expr.getConcrValue() if hasattr(expr, 'getConcrValue') else int(expr)
						return self._constant(concrete_val, solver)
					return self._getIntegerVariable(expr.name,solver)
				else:
					# Handle 'const' variable specially - it's not a real variable
					if expr.name == 'const':
						# 'const' is a placeholder for concrete constants
						# Return concrete value as Python int
						concrete_val = expr.getConcrValue() if hasattr(expr, 'getConcrValue') else int(expr)
						return concrete_val
					return env[expr.name]
			else:
				return self._astToZ3Expr(expr.expr,solver,env)

		elif isinstance(expr, SymbolicStr):
			# For string values, we need to handle them specially
			# Since Z3 doesn't directly support strings in this implementation,
			# we'll return the concrete string value for evaluation purposes
			if env is None:
				# In symbolic mode, we need to think about how to handle strings
				# For now, treat them as unsupported for Z3 solving
				# But allow them to pass through for concrete evaluation
				# We'll return the concrete value as a string constant
				# This will be used when evaluating predicates concretely
				concrete_val = expr.getConcrValue() if hasattr(expr, 'getConcrValue') else str(expr)
				# Return as a string - note: Z3 doesn't have string support here
				# This may cause issues if used in constraints
				# For now, just return the concrete value
				return concrete_val
			else:
				# In concrete evaluation mode, return the concrete string
				concrete_val = expr.getConcrValue() if hasattr(expr, 'getConcrValue') else str(expr)
				return concrete_val

		elif isinstance(expr, SymbolicType):
			utils.crash("{} is an unsupported SymbolicType of {}".
						format(expr, type(expr)))

		elif isinstance(expr, int):
			if env == None:
				return self._constant(expr,solver)
			else:
				return expr
		elif isinstance(expr, str):
			# Handle string literals - they may appear in script mode
			# For symbolic execution, we need to handle strings properly
			if env is None:
				# In symbolic mode, return the string as a constant
				# This may need to be enhanced for full string support
				# For now, return as a concrete string
				return expr
			else:
				# In concrete evaluation mode, just return the string
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
