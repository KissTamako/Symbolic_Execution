# Copyright: see copyright.txt

from collections import deque
import logging
import os

from .z3_wrap import Z3Wrapper
from .solver import SolverWrapper
from .path_to_constraint import PathToConstraint
from .invocation import FunctionInvocation
from .symbolic_types import symbolic_type, SymbolicType
from .trace import record_execution, get_trace_recorder
from .input_model import get_input_model

log = logging.getLogger("se.conc")

class ExplorationEngine:
	def __init__(self, funcinv, solver="z3"):
		self.invocation = funcinv
		# the input to the function
		self.symbolic_inputs = {}  # string -> SymbolicType
		# initialize
		for n in funcinv.getNames():
			self.symbolic_inputs[n] = funcinv.createArgumentValue(n)

		self.constraints_to_solve = deque([])
		self.num_processed_constraints = 0

		self.path = PathToConstraint(lambda c : self.addConstraint(c))
		# link up SymbolicObject to PathToConstraint in order to intercept control-flow
		symbolic_type.SymbolicObject.SI = self.path

		if solver == "z3":
			self.solver = Z3Wrapper()
		elif solver == "cvc":
			self.solver = SolverWrapper(solver_type="cvc4")
		else:
			raise Exception("Unknown solver %s" % solver)

		# outputs
		self.generated_inputs = []
		self.execution_return_values = []

	def addConstraint(self, constraint):
		self.constraints_to_solve.append(constraint)
		# make sure to remember the input that led to this constraint
		# Save concrete values, not symbolic objects
		constraint.inputs = self._getConcreteInputs()

	def explore(self, max_iterations=0):
		self._oneExecution()
		
		iterations = 1
		if max_iterations != 0 and iterations >= max_iterations:
			log.debug("Maximum number of iterations reached, terminating")
			return self.execution_return_values

		while not self._isExplorationComplete():
			selected = self.constraints_to_solve.popleft()
			if selected.processed:
				continue
			self._setInputs(selected.inputs)			

			log.info("Selected constraint %s" % selected)
			asserts, query = selected.getAssertsAndQuery()
			model = self.solver.findCounterexample(asserts, query)

			if model == None:
				continue
			else:
				for name in model.keys():
					self._updateSymbolicParameter(name,model[name])

			self._oneExecution(selected)

			iterations += 1			
			self.num_processed_constraints += 1

			if max_iterations != 0 and iterations >= max_iterations:
				log.info("Maximum number of iterations reached, terminating")
				break

		return self.generated_inputs, self.execution_return_values, self.path

	# private

	def _updateSymbolicParameter(self, name, val):
		self.symbolic_inputs[name] = self.invocation.createArgumentValue(name,val)

	def _getInputs(self):
		return self.symbolic_inputs.copy()

	def _getConcreteInputs(self):
		"""Get concrete values for all symbolic inputs."""
		return {k: self._getConcrValue(v) for k, v in self.symbolic_inputs.items()}

	def _setInputs(self,d):
		"""Set inputs from concrete values dictionary."""
		# d should be concrete values, need to recreate symbolic objects
		self.symbolic_inputs = {}
		for name, value in d.items():
			# Recreate symbolic parameter using invocation
			self.symbolic_inputs[name] = self.invocation.createArgumentValue(name, value)

	def _isExplorationComplete(self):
		num_constr = len(self.constraints_to_solve)
		if num_constr == 0:
			log.info("Exploration complete")
			return True
		else:
			log.info("%d constraints yet to solve (total: %d, already solved: %d)" % (num_constr, self.num_processed_constraints + num_constr, self.num_processed_constraints))
			return False

	def _getConcrValue(self,v):
		if isinstance(v,SymbolicType):
			return v.getConcrValue()
		else:
			return v

	def _recordInputs(self):
		args = self.symbolic_inputs
		inputs = [ (k,self._getConcrValue(args[k])) for k in args ]
		self.generated_inputs.append(inputs)
		print(inputs)
		
	def _oneExecution(self,expected_path=None):
		self._recordInputs()
		self.path.reset(expected_path)
		
		# Record execution trace
		concrete_inputs = {k: self._getConcrValue(v) for k, v in self.symbolic_inputs.items()}
		
		ret = self.invocation.callFunction(self.symbolic_inputs)
		print(ret)
		self.execution_return_values.append(ret)
		
		# Record execution trace
		try:
			record_execution(
				concrete_inputs=concrete_inputs,
				return_value=ret,
				exception=None,
				branch_trace=[],  # TODO: Week 3 - collect actual branch trace
				path_id=f"path_{len(self.execution_return_values)-1}"
			)
		except Exception as e:
			log.warning(f"Failed to record execution trace: {e}")
