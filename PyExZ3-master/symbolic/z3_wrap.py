# Copyright: see copyright.txt

import sys
import ast
import logging

from z3 import *
from .z3_expr.integer import Z3Integer
from .z3_expr.bitvector import Z3BitVector

log = logging.getLogger("se.z3")

class Z3Wrapper(object):
	def __init__(self):
		self.N = 32
		self.asserts = None
		self.query = None
		self.use_lia = True
		self.z3_expr = None

	def findCounterexample(self, asserts, query):
		"""Tries to find a counterexample to the query while
	  	 asserts remains valid."""
		self.solver = Solver()
		self.query = query
		self.asserts = self._coneOfInfluence(asserts,query)
		res = self._findModel()
		log.debug("Query -- %s" % self.query)
		log.debug("Asserts -- %s" % asserts)
		log.debug("Cone -- %s" % self.asserts)
		log.debug("Result -- %s" % res)
		return res

	# private

	# this is very inefficient
	def _coneOfInfluence(self,asserts,query):
		cone = []
		cone_vars = set()
		
		# If query is None, start with empty variable set
		if query is not None and hasattr(query, 'getVars'):
			cone_vars = set(query.getVars())
		
		ws = [ a for a in asserts if len(set(a.getVars()) & cone_vars) > 0 ]
		remaining = [ a for a in asserts if a not in ws ]
		
		# If cone_vars is empty, all assertions are relevant
		if len(cone_vars) == 0:
			return asserts
			
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
		# Try QF_LIA first (as it may fairly easily recognize unsat instances)
		if self.use_lia:
			self.solver.push()
			self.z3_expr = Z3Integer()
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
		return res

	def _setAssertsQuery(self):
		self.z3_expr = Z3BitVector(self.N)
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
			# Skip internal 'const' variable
			if name == 'const':
				continue
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
	
	def build_solver(self, asserts, query, negate_query=True):
		"""
		Build a Z3 solver with given assertions and query.
		
		Args:
			asserts: List of assertions
			query: Query predicate
			negate_query: Whether to negate the query (default: True for counterexample finding)
		
		Returns:
			Z3 solver object
		"""
		self.solver = Solver()
		self.query = query
		self.asserts = self._coneOfInfluence(asserts, query)
		
		# Add assertions to solver
		self.z3_expr = Z3Integer() if self.use_lia else Z3BitVector()
		self.z3_expr.toZ3(self.solver, self.asserts, None)  # Add assertions only
		
		# Add query (negated if requested)
		if query is not None:
			if negate_query:
				# For counterexample finding, we want to find models where query is false
				negated_query = self.z3_expr.predToZ3(query, self.solver)
				if negated_query is not None:
					self.solver.add(Not(negated_query))
			else:
				# For validation, add query as assertion
				query_expr = self.z3_expr.predToZ3(query, self.solver)
				if query_expr is not None:
					self.solver.add(query_expr)
		
		return self.solver
	
	def export_current_query_to_smt2(self, output_path, solver_logic="QF_LIA"):
		"""
		Export current solver state to SMTLIB2 format.
		
		Args:
			output_path: Path to save SMT2 file
			solver_logic: SMT solver logic to use
		
		Returns:
			Path to saved SMT2 file, or None if export failed
		"""
		if self.solver is None:
			log.warning("No solver initialized. Call build_solver() first.")
			return None
		
		try:
			# Get solver assertions as SMTLIB2 string
			smt2_str = self.solver.to_smt2()
			
			# Write to file
			with open(output_path, 'w') as f:
				f.write(smt2_str)
			
			log.debug(f"Exported solver state to {output_path}")
			return output_path
		except Exception as e:
			log.error(f"Failed to export SMT2: {e}")
			return None
	
	def export_constraints_to_smt2(self, asserts, query, output_path, negate_query=True, solver_logic="QF_LIA"):
		"""
		Export constraints to SMTLIB2 format.
		
		Args:
			asserts: List of assertions
			query: Query predicate
			output_path: Path to save SMT2 file
			negate_query: Whether to negate the query
			solver_logic: SMT solver logic
		
		Returns:
			Path to saved SMT2 file, or None if export failed
		"""
		# Build solver with constraints
		self.build_solver(asserts, query, negate_query)
		
		# Export to SMT2
		return self.export_current_query_to_smt2(output_path, solver_logic)

