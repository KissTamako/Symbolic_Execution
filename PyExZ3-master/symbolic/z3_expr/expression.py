import utils

from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types.symbolic_bool import SymbolicBool
from symbolic.symbolic_types.symbolic_type import SymbolicType
from z3 import *

class Z3Expression(object):
	def __init__(self, enable_simplify=False):
		self.z3_vars = {}
		self.enable_simplify = enable_simplify

	def toZ3(self,solver,asserts,query):
		self.z3_vars = {}
		assert_exprs = [self.predToZ3(p,solver) for p in asserts]
		query_expr = Not(self.predToZ3(query,solver))
		
		if self.enable_simplify:
			assert_exprs = [simplify(e) for e in assert_exprs]
			query_expr = simplify(query_expr)
		
		solver.assert_exprs(assert_exprs)
		solver.assert_exprs(query_expr)

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
		raise NotImplementedException

	def _getIntegerVariable(self,name,solver):
		if name not in self.z3_vars:
			self.z3_vars[name] = self._variable(name,solver)
		return self.z3_vars[name]

	def _variable(self,name,solver):
		raise NotImplementedException

	def _constant(self,v,solver):
		raise NotImplementedException

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

			# 单参数操作
			if op == "abs":
				if len(args) != 1:
					utils.crash("Expected 1 argument for abs operation, got %d" % len(args))
				return If(args[0] >= 0, args[0], -args[0]) if env is None else abs(args[0])
			elif op == "not":
				if len(args) != 1:
					utils.crash("Expected 1 argument for not operation, got %d" % len(args))
				# 确保参数是布尔类型，然后再应用Not
				if env is None:
					if not is_bool(args[0]):
						# 将非布尔值转换为布尔值（0为False，非0为True）
						bool_expr = args[0] != self._constant(0, solver)
						return Not(bool_expr)
					else:
						return Not(args[0])
				else:
					return not args[0]

			# 双参数操作
			if len(args) != 2:
				utils.crash("Expected 2 arguments for binary operation, got %d" % len(args))
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
			elif op == "=":
				return self._wrapIf(z3_l == z3_r,solver,env)
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
					return self._getIntegerVariable(expr.name,solver)
				else:
					return env[expr.name]
			else:
				return self._astToZ3Expr(expr.expr,solver,env)

		elif isinstance(expr, SymbolicBool):
			if expr.isVariable():
				if env == None:
					return self._getIntegerVariable(expr.name,solver)
				else:
					return env[expr.name]
			else:
				return self._astToZ3Expr(expr.expr,solver,env)

		elif isinstance(expr, SymbolicType):
			utils.crash("{} is an unsupported SymbolicType of {}".
							format(expr, type(expr)))

		elif isinstance(expr, int):
			if env == None:
				return self._constant(expr,solver)
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
