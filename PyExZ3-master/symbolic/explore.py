# Copyright: see copyright.txt

from collections import deque
import logging
import os

from .z3_wrap import Z3Wrapper
from .path_to_constraint import PathToConstraint
from .invocation import FunctionInvocation
from .symbolic_types import symbolic_type, SymbolicType
from .exporters import JSONExporter, SMTExporter
log = logging.getLogger("se.conc")

class ExplorationEngine:
	def __init__(self, invocation, solver="z3", output_dir="./outputs", enable_frontier_dedup=False, search_strategy='bfs', enable_simplify=False, enable_prefix_dedup=False, max_prefix_length=2, enable_incremental=False, dump_all_executions=False):
		self.invocation = invocation
		# the input to the function or script
		self.symbolic_inputs = {}  # string -> SymbolicType
		# initialize
		if hasattr(invocation, 'getNames'):
			for n in invocation.getNames():
				self.symbolic_inputs[n] = invocation.createArgumentValue(n)

		self.constraints_to_solve = deque([])
		self.num_processed_constraints = 0
		
		# Frontier约束去重
		self.enable_frontier_dedup = enable_frontier_dedup
		self.seen_constraint_hashes = set()
		
		# 前缀去重（简化版）
		self.enable_prefix_dedup = enable_prefix_dedup
		self.max_prefix_length = max_prefix_length
		self.seen_prefixes = set()
		
		# 搜索策略：'bfs'（广度优先）或 'dfs'（深度优先）
		self.search_strategy = search_strategy.lower()
		if self.search_strategy not in ['bfs', 'dfs']:
			log.warning(f"Unknown search strategy: {search_strategy}, using 'bfs' instead")
			self.search_strategy = 'bfs'

		self.path = PathToConstraint(lambda c : self.addConstraint(c))
		# link up SymbolicObject to PathToConstraint in order to intercept control-flow
		symbolic_type.SymbolicObject.SI = self.path

		if solver == "z3":
			self.solver = Z3Wrapper(enable_simplify=enable_simplify, enable_incremental=enable_incremental)
		elif solver == "cvc":
			from .cvc_wrap import CVCWrapper
			self.solver = CVCWrapper()
		else:
			raise Exception("Unknown solver %s" % solver)

		# outputs
		self.generated_inputs = []
		self.execution_return_values = []
		self.path_lengths_list = []
		self.branch_traces_list = []
		self.symbolic_inputs_list = []  # 保存每次执行的 symbolic_inputs
		self.dump_all_executions = dump_all_executions  # 是否导出所有执行的详细信息
		
		# exporters
		self.output_dir = output_dir
		self.json_exporter = JSONExporter(output_dir)
		self.smt_exporter = SMTExporter(output_dir)

	def addConstraint(self, constraint):
		# make sure to remember the input that led to this constraint
		constraint.inputs = self._getInputs()
		
		# 如果启用了前缀去重（简化版）
		if self.enable_prefix_dedup:
			# 只对路径长度较短的约束进行前缀检查
			path_length = constraint.getLength()
			if path_length <= self.max_prefix_length:
				prefix_key = self._getPathPrefixKey(constraint)
				if prefix_key in self.seen_prefixes:
					log.debug(f"Prefix already exists, skipping: {prefix_key}")
					return
				self.seen_prefixes.add(prefix_key)
		
		# 如果启用了Frontier约束去重
		if self.enable_frontier_dedup:
			# 使用简单的哈希来判断约束是否已存在
			constraint_hash = self._getSimpleConstraintHash(constraint)
			if constraint_hash in self.seen_constraint_hashes:
				log.debug(f"Constraint already exists, skipping: {constraint_hash}")
				return
			self.seen_constraint_hashes.add(constraint_hash)
		
		# 根据搜索策略选择插入方式
		if self.search_strategy == 'bfs':
			# BFS：在末尾添加（FIFO）
			self.constraints_to_solve.append(constraint)
		else:  # dfs
			# DFS：在开头添加（LIFO）
			self.constraints_to_solve.appendleft(constraint)
	
	def _getSimpleConstraintHash(self, constraint):
		"""生成约束的简单哈希值
		
		使用Python内置的hash函数，基于约束的对象标识
		
		Args:
			constraint: Constraint对象
			
		Returns:
			constraint_hash: 约束的哈希值
		"""
		# 使用约束对象的id作为简单的哈希值
		return id(constraint)
	
	def _getPathPrefixKey(self, constraint):
		"""生成路径前缀的唯一键
		
		Args:
			constraint: Constraint对象
			
		Returns:
			prefix_key: 路径前缀的唯一键
		"""
		# 收集路径上的谓词字符串表示
		predicate_strs = []
		tmp = constraint
		while tmp.predicate is not None:
			pred_str = str(tmp.predicate.symtype.expr)
			predicate_strs.append(pred_str)
			tmp = tmp.parent
		
		# 反转并连接
		predicate_strs.reverse()
		return "|".join(predicate_strs)

	def explore(self, max_iterations=0, dump_constraints=False, dump_trace=False, dump_semantics=False):
		print("Starting explore method...")
		print(f"max_iterations: {max_iterations}")
		print(f"dump_constraints: {dump_constraints}")
		print(f"dump_trace: {dump_trace}")
		print(f"dump_semantics: {dump_semantics}")
		
		self._oneExecution()
		print("First execution completed")
		
		iterations = 1
		if max_iterations != 0 and iterations >= max_iterations:
			log.debug("Maximum number of iterations reached, terminating")
			if dump_constraints or dump_trace or dump_semantics:
				self._export_results()
			print("Returning early due to max iterations")
			return self.generated_inputs, self.execution_return_values, self.path

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

		if dump_constraints or dump_trace or dump_semantics:
			self._export_results()
		return self.generated_inputs, self.execution_return_values, self.path

	def _export_results(self):
		"""Export results to files"""
		# Export path information
		path_data = self.json_exporter.export_path(self.path, self.symbolic_inputs, self.execution_return_values)
		
		# Export branch trace
		current_path = self.path.get_current_path()
		self.json_exporter.export_branch_trace(current_path)
		
		# Export semantic tags
		self.json_exporter.export_semantic_tags(self.path)
		
		# Export frontier constraints
		frontier = self.path.get_frontier_constraints()
		self.json_exporter.export_frontier(frontier)
		
		# Prepare execution summary data
		execution_data = {
			'generated_inputs': self.generated_inputs,
			'return_values': self.execution_return_values,
			'branch_traces': self.branch_traces_list,
			'path_lengths': self.path_lengths_list
		}
		
		# Export execution summary
		self.json_exporter.export_execution_summary(execution_data)
		self.smt_exporter.export_execution_summary(execution_data)
		
		# Export SMT files for path constraints
		if frontier:
			# Get assertions and query from the first frontier constraint as an example
			asserts, query = frontier[0].getAssertsAndQuery()
			self.smt_exporter.export_path(self.solver, asserts, query)
			self.smt_exporter.export_frontier(self.solver, frontier)
		
		# 导出所有执行的详细信息（如果启用）
		if self.dump_all_executions:
			self.json_exporter.export_all_executions(
				self.symbolic_inputs_list, 
				self.execution_return_values, 
				self.branch_traces_list
			)

	# private

	def _updateSymbolicParameter(self, name, val):
		self.symbolic_inputs[name] = self.invocation.createArgumentValue(name,val)

	def _getInputs(self):
		return self.symbolic_inputs.copy()

	def _setInputs(self,d):
		self.symbolic_inputs = d

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
		
		# 保存当前的 symbolic_inputs（在执行前保存，因为执行可能会修改它）
		self.symbolic_inputs_list.append(self.symbolic_inputs.copy())
		
		if hasattr(self.invocation, 'callFunction'):
			ret = self.invocation.callFunction(self.symbolic_inputs)
		elif hasattr(self.invocation, 'execute'):
			ret = self.invocation.execute(self.symbolic_inputs)
		else:
			raise Exception("Unknown invocation type")
		print(ret)
		self.execution_return_values.append(ret)
		
		# 记录当前路径的长度和分支跟踪
		current_path = self.path.get_current_path()
		self.path_lengths_list.append(len(current_path))
		self.branch_traces_list.append(current_path.copy())

