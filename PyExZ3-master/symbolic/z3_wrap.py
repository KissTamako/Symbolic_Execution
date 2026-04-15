# Copyright: see copyright.txt

import sys
import ast
import logging
from collections import OrderedDict

from z3 import *
from .z3_expr.integer import Z3Integer
from .z3_expr.bitvector import Z3BitVector
from .z3_expr.float import Z3Float
from .symbolic_types import SymbolicFloat

log = logging.getLogger("se.z3")

class Z3Wrapper(object):
	def __init__(self, max_cache_size=1000, enable_simplify=False, enable_incremental=False):
		self.N = 32
		self.asserts = None
		self.query = None
		self.use_lia = True
		self.z3_expr = None
		# UNSAT缓存：使用OrderedDict实现LRU缓存
		self.max_cache_size = max_cache_size
		self.unsat_cache = OrderedDict()
		# 性能统计
		self.stats = {
			'total_calls': 0,
			'cache_hits': 0,
			'cache_misses': 0
		}
		# 约束简化
		self.enable_simplify = enable_simplify
		# 增量求解
		self.enable_incremental = enable_incremental
		if self.enable_incremental:
			self.persistent_solver = Solver()

	def findCounterexample(self, asserts, query):
		"""Tries to find a counterexample to the query while
	  	 asserts remains valid."""
		# 更新统计信息
		self.stats['total_calls'] += 1
		
		# 生成约束组合的唯一标识，用于UNSAT缓存
		constraint_key = self._getConstraintKey(asserts, query)
		
		# 检查UNSAT缓存
		if constraint_key in self.unsat_cache:
			self.stats['cache_hits'] += 1
			# 将访问的键移到末尾，表示最近使用
			self.unsat_cache.move_to_end(constraint_key)
			log.debug(f"UNSAT cache hit for constraint: {constraint_key}")
			return None
		
		self.stats['cache_misses'] += 1
		self.solver = Solver()
		self.query = query
		self.asserts = self._coneOfInfluence(asserts,query)
		res = self._findModel()
		
		# 如果结果是None（UNSAT），则添加到缓存中
		if res is None:
			# 如果缓存已满，删除最久未使用的条目
			if len(self.unsat_cache) >= self.max_cache_size:
				removed_key = self.unsat_cache.popitem(last=False)
				log.debug(f"Removed from UNSAT cache (LRU): {removed_key}")
			# 添加新条目到缓存
			self.unsat_cache[constraint_key] = True
			log.debug(f"Added to UNSAT cache: {constraint_key}")
		
		log.debug("Query -- %s" % self.query)
		log.debug("Asserts -- %s" % self.asserts)
		log.debug("Cone -- %s" % self.asserts)
		log.debug("Result -- %s" % res)
		return res
	
	def _getConstraintKey(self, asserts, query):
		"""生成约束组合的唯一标识
		
		Args:
			asserts: 断言列表
			query: 查询谓词
			
		Returns:
			constraint_key: 约束组合的唯一标识
		"""
		# 将约束转换为字符串表示，用于生成唯一标识
		# 注意：这里使用简化的方法，实际应用中可能需要更复杂的实现
		assert_strs = []
		for assert_pred in asserts:
			if hasattr(assert_pred, 'symtype'):
				assert_strs.append(str(assert_pred.symtype.expr))
		
		query_str = str(query.symtype.expr) if hasattr(query, 'symtype') else str(query)
		
		# 排序以确保相同约束的不同顺序生成相同的key
		assert_strs.sort()
		
		return "|".join(assert_strs) + "||" + query_str
	
	def getStats(self):
		"""获取性能统计信息
		
		Returns:
			stats: 性能统计字典
		"""
		return self.stats.copy()
	
	def resetStats(self):
		"""重置性能统计信息"""
		self.stats = {
			'total_calls': 0,
			'cache_hits': 0,
			'cache_misses': 0
		}

	# private

	# this is very inefficient
	def _coneOfInfluence(self,asserts,query):
		cone = []
		cone_vars = set(query.getVars())
		ws = [ a for a in asserts if len(set(a.getVars()) & cone_vars) > 0 ]
		remaining = [ a for a in asserts if a not in ws ]
		while len(ws) > 0:
			a = ws.pop()
			a_vars = set(a.getVars())
			cone_vars = cone_vars.union(a_vars)
			cone.append(a)
			new_ws = [ a for a in remaining if len(set(a.getVars()) & cone_vars) > 0 ]
			remaining = [ a for a in remaining if a not in new_ws ]
			ws = ws + new_ws
		return cone

	def _findModel(self):
		# Check if we're dealing with float expressions
		has_float = False
		for a in self.asserts:
			if isinstance(a.symtype, SymbolicFloat):
				has_float = True
				break
		if isinstance(self.query.symtype, SymbolicFloat):
			has_float = True
		
		# If we have float expressions, use Z3Float
		if has_float:
			self.solver.push()
			self.z3_expr = Z3Float(self.enable_simplify)
			self.z3_expr.toZ3(self.solver, self.asserts, self.query)
			res = self.solver.check()
			if res == sat:
				# For simplicity, we'll just return a dummy model
				# In a real implementation, we would extract float values from the model
				return {}
			elif res == unsat:
				return None
			else:
				return None
		
		# Try QF_LIA first (as it may fairly easily recognize unsat instances)
		if self.use_lia:
			self.solver.push()
			self.z3_expr = Z3Integer(self.enable_simplify)
			self.z3_expr.toZ3(self.solver,self.asserts,self.query)
			res = self.solver.check()
			#print(self.solver.assertions)
			self.solver.pop()
			if res == unsat:
				return None

		# now, go for SAT with bounds
		self.N = 32
		self.bound = (1 << 4) - 1
		while self.N <= 64:
			self.solver.push()
			(ret,mismatch) = self._findModel2()
			if (not mismatch):
				break
			self.solver.pop()
			self.N = self.N+8
			if self.N <= 64: print("expanded bit width to "+str(self.N)) 
		#print("Assertions")
		#print(self.solver.assertions())
		if ret == unsat:
			res = None
		elif ret == unknown:
			res = None
		elif not mismatch:
			res = self._getModel()
		else:
			res = None
		if self.N<=64: self.solver.pop()
		
		# 特殊处理：如果res为None且N达到64位，尝试使用Z3Integer再次求解
		# 这是为了处理sys.maxsize+1的情况，因为Z3Integer使用的是无限精度整数
		if res is None and self.N >= 64:
			self.solver.push()
			z3_int = Z3Integer(self.enable_simplify)
			z3_int.toZ3(self.solver, self.asserts, self.query)
			res = self.solver.check()
			if res == sat:
				# 提取模型
				model = self.solver.model()
				z3_vars = {}
				for name in model.decls():
					z3_vars[name.name()] = model[name].as_long()
				self.solver.pop()
				return z3_vars
			else:
				self.solver.pop()
		
		return res

	def _setAssertsQuery(self):
		# Check if we're dealing with float expressions
		has_float = False
		for a in self.asserts:
			if isinstance(a.symtype, SymbolicFloat):
				has_float = True
				break
		if isinstance(self.query.symtype, SymbolicFloat):
			has_float = True
		
		# If we have float expressions, use Z3Float
		if has_float:
			self.z3_expr = Z3Float(self.enable_simplify)
		else:
			self.z3_expr = Z3BitVector(self.N, self.enable_simplify)
		
		self.z3_expr.toZ3(self.solver,self.asserts,self.query)

	def _findModel2(self):
		self._setAssertsQuery()
		int_vars = self.z3_expr.getIntVars()
		res = unsat
		while res == unsat and self.bound <= (1 << (self.N-1))-1:
			self.solver.push()
			constraints = self._boundIntegers(int_vars,self.bound)
			self.solver.assert_exprs(constraints)
			res = self.solver.check()
			if res == unsat:
				self.bound = (self.bound << 1)+1
				self.solver.pop()
		if res == sat:
			# Does concolic agree with Z3? If not, it may be due to overflow
			model = self._getModel()
			#print("Match?")
			#print(self.solver.assertions)
			self.solver.pop()
			mismatch = False
			for a in self.asserts:
				eval = self.z3_expr.predToZ3(a,self.solver,model)
				if (not eval):
					mismatch = True
					break
			if (not mismatch):
				mismatch = not (not self.z3_expr.predToZ3(self.query,self.solver,model))
			#print(mismatch)
			return (res,mismatch)
		elif res == unknown:
			self.solver.pop()
		return (res,False)

	def _getModel(self):
		res = {}
		model = self.solver.model()
		for name in self.z3_expr.z3_vars.keys():
			try:
				ce = model.eval(self.z3_expr.z3_vars[name])
				res[name] = ce.as_signed_long()
			except:
				pass
		return res
	
	def _boundIntegers(self,vars,val):
		bval = BitVecVal(val,self.N,self.solver.ctx)
		bval_neg = BitVecVal(-val-1,self.N,self.solver.ctx)
		return And([ v <= bval for v in vars]+[ bval_neg <= v for v in vars])

