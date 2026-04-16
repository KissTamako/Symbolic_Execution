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
	def __init__(self, invocation, solver="z3", output_dir="./outputs", enable_frontier_dedup=False, search_strategy='bfs', enable_simplify=False, enable_prefix_dedup=False, max_prefix_length=2, enable_incremental=False, dump_all_executions=False, execution_mode="symbolic", concolic_iterations=10, concrete_value_strategy="random", path_selection_strategy='bfs', enable_path_pruning=False, enable_hybrid_search=False, path_priority_weight=0.5):
		self.invocation = invocation
		# the input to the function or script
		self.symbolic_inputs = {}  # string -> SymbolicType
		# initialize
		if hasattr(invocation, 'getNames'):
			for n in invocation.getNames():
				self.symbolic_inputs[n] = invocation.createArgumentValue(n)
		
		# Execution mode: symbolic, concolic, or concrete
		self.execution_mode = execution_mode.lower()
		if self.execution_mode not in ['symbolic', 'concolic', 'concrete']:
			log.warning(f"Unknown execution mode: {execution_mode}, using 'symbolic' instead")
			self.execution_mode = 'symbolic'
		
		# Concolic execution parameters
		self.concolic_iterations = concolic_iterations
		self.concrete_value_strategy = concrete_value_strategy.lower()
		if self.concrete_value_strategy not in ['random', 'guided', 'hybrid']:
			log.warning(f"Unknown concrete value strategy: {concrete_value_strategy}, using 'random' instead")
			self.concrete_value_strategy = 'random'

		self.constraints_to_solve = deque([])
		self.num_processed_constraints = 0
		
		# Frontier约束去重
		self.enable_frontier_dedup = enable_frontier_dedup
		self.seen_constraint_hashes = set()
		
		# 前缀去重（简化版）
		self.enable_prefix_dedup = enable_prefix_dedup
		self.max_prefix_length = max_prefix_length
		self.seen_prefixes = set()
		
		# 搜索策略：'bfs'（广度优先）、'dfs'（深度优先）或 'smart'（智能选择）
		self.path_selection_strategy = path_selection_strategy.lower()
		if self.path_selection_strategy not in ['bfs', 'dfs', 'smart']:
			log.warning(f"Unknown path selection strategy: {path_selection_strategy}, using 'bfs' instead")
			self.path_selection_strategy = 'bfs'
		
		# 路径剪枝
		self.enable_path_pruning = enable_path_pruning
		
		# 混合搜索策略
		self.enable_hybrid_search = enable_hybrid_search
		self.hybrid_search_switch_iteration = 5  # 在第5次迭代后切换搜索策略
		
		# 路径优先级权重
		self.path_priority_weight = path_priority_weight
		
		# 代码覆盖率跟踪
		self.code_coverage = set()
		
		# 已探索的路径
		self.explored_paths = set()

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
		
		# 如果启用了路径剪枝
		if self.enable_path_pruning:
			if self._should_prune_path(constraint):
				log.debug("Pruning path")
				return
		
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
		
		# 根据路径选择策略选择插入方式
		if self.path_selection_strategy == 'smart':
			# 智能选择：根据路径优先级插入
			priority = self._calculate_path_priority(constraint)
			constraint.priority = priority
			# 按优先级插入到合适的位置
			inserted = False
			for i, c in enumerate(self.constraints_to_solve):
				if not hasattr(c, 'priority'):
					c.priority = self._calculate_path_priority(c)
				if priority > c.priority:
					self.constraints_to_solve.insert(i, constraint)
					inserted = True
					break
			if not inserted:
				self.constraints_to_solve.append(constraint)
		elif self.path_selection_strategy == 'bfs':
			# BFS：在末尾添加（FIFO）
			self.constraints_to_solve.append(constraint)
		else:  # dfs
			# DFS：在开头添加（LIFO）
			self.constraints_to_solve.appendleft(constraint)
		
	def _should_prune_path(self, constraint):
		"""判断是否应该剪枝路径"""
		# 检查路径是否已被探索
		path_key = self._getPathKey(constraint)
		if path_key in self.explored_paths:
			return True
		
		# 检查路径长度是否过长
		path_length = constraint.getLength()
		if path_length > 50:  # 路径长度超过50时剪枝
			return True
		
		# 检查语义相似性
		if self._is_semantically_similar(constraint):
			return True
		
		# 检查执行成本
		if self._is_execution_cost_high(constraint):
			return True
		
		# 检查循环
		if self._has_cycles(constraint):
			return True
		
		return False
		
	def _calculate_path_priority(self, constraint):
		"""计算路径优先级"""
		# 简化路径优先级计算，确保所有约束都能被处理
		# 计算路径长度（较短的路径优先级较高）
		path_length = constraint.getLength()
		length_score = 1.0 / (path_length + 1)
		
		# 计算路径覆盖率（覆盖新代码的路径优先级较高）
		coverage_score = self._calculate_path_coverage_score(constraint)
		
		# 综合计算优先级（简化版）
		priority = (length_score * 0.6 + coverage_score * 0.4) * 100
		
		return priority
		
	def _calculate_path_complexity(self, constraint):
		"""计算路径复杂度"""
		# 简单实现：使用路径长度作为复杂度
		return constraint.getLength()
		
	def _calculate_path_coverage_score(self, constraint):
		"""计算路径覆盖率分数"""
		# 简单实现：假设每条路径都能覆盖新代码
		return 1.0
		
	def _calculate_solving_difficulty_score(self, constraint):
		"""计算约束求解难度分数"""
		# 简单实现：基于约束的长度和复杂度评估求解难度
		# 约束越长、越复杂，求解难度越高
		
		# 获取约束的断言和查询
		asserts, query = constraint.getAssertsAndQuery()
		
		# 计算约束的总长度
		constraint_length = len(str(asserts)) + len(str(query))
		
		# 计算求解难度分数（难度越低，分数越高）
		difficulty_score = 1.0 / (1.0 + constraint_length / 1000.0)
		
		return difficulty_score
		
	def _calculate_execution_history_score(self, constraint):
		"""计算执行历史分数"""
		# 简单实现：假设所有路径的执行历史分数相同
		# 实际应用中，可以记录每条路径的执行时间，执行时间越短，分数越高
		return 1.0
		
	def _get_dynamic_weights(self):
		"""获取动态权重"""
		# 基于执行情况动态调整各维度的权重
		# 在执行初期，优先考虑覆盖率贡献
		# 在执行后期，优先考虑约束求解难度
		
		# 计算执行进度
		total_constraints = len(self.constraints_to_solve) + self.num_processed_constraints
		if total_constraints == 0:
			execution_progress = 0.0
		else:
			execution_progress = self.num_processed_constraints / total_constraints
		
		# 根据执行进度调整权重
		if execution_progress < 0.3:
			# 执行初期，优先考虑覆盖率
			return {
				'length': 0.2,
				'complexity': 0.2,
				'coverage': 0.3,
				'solving': 0.2,
				'history': 0.1
			}
		elif execution_progress < 0.7:
			# 执行中期，平衡各维度
			return {
				'length': 0.2,
				'complexity': 0.2,
				'coverage': 0.2,
				'solving': 0.2,
				'history': 0.2
			}
		else:
			# 执行后期，优先考虑约束求解难度
			return {
				'length': 0.1,
				'complexity': 0.1,
				'coverage': 0.2,
				'solving': 0.4,
				'history': 0.2
			}
		
	def _is_semantically_similar(self, constraint):
		"""检查路径是否语义相似"""
		# 简单实现：基于约束的字符串表示检查相似性
		# 实际应用中，可以使用更复杂的语义相似性算法
		
		# 获取当前约束的字符串表示
		current_constraint_str = str(constraint)
		
		# 检查是否与已探索的约束语义相似
		# 这里使用简单的字符串相似度检查
		for explored_path in self.explored_paths:
			if explored_path in current_constraint_str or current_constraint_str in explored_path:
				return True
		
		return False
		
	def _is_execution_cost_high(self, constraint):
		"""检查路径的执行成本是否过高"""
		# 简单实现：基于约束的长度和复杂度评估执行成本
		# 约束越长、越复杂，执行成本越高
		
		# 获取约束的断言和查询
		asserts, query = constraint.getAssertsAndQuery()
		
		# 计算约束的总长度
		constraint_length = len(str(asserts)) + len(str(query))
		
		# 执行成本过高的阈值
		execution_cost_threshold = 5000
		
		return constraint_length > execution_cost_threshold
		
	def _has_cycles(self, constraint):
		"""检查路径是否包含循环"""
		# 简单实现：基于路径的长度和结构检查循环
		# 实际应用中，可以使用更复杂的循环检测算法
		
		# 检查路径长度
		path_length = constraint.getLength()
		if path_length < 3:
			return False
		
		# 收集路径上的谓词
		predicates = []
		tmp = constraint
		while tmp.predicate is not None:
			pred_str = str(tmp.predicate.symtype.expr)
			predicates.append(pred_str)
			tmp = tmp.parent
		
		# 检查是否有重复的谓词（可能表示循环）
		if len(predicates) != len(set(predicates)):
			return True
		
		return False
		
	def _getPathKey(self, constraint):
		"""生成路径的唯一键"""
		# 收集路径上的谓词字符串表示
		predicate_strs = []
		tmp = constraint
		while tmp.predicate is not None:
			pred_str = str(tmp.predicate.symtype.expr)
			predicate_strs.append(pred_str)
			tmp = tmp.parent
		
		# 反转并连接
		predicate_strs.reverse()
		return "|" + "|".join(predicate_strs)
	
	def _getSimpleConstraintHash(self, constraint):
		"""生成约束的简单哈希值
		
		基于约束的内容生成哈希值，支持跨会话的约束去重
		
		Args:
			constraint: Constraint对象
			
		Returns:
			constraint_hash: 约束的哈希值
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
		constraint_key = "|".join(predicate_strs)
		
		# 基于约束内容生成哈希值
		return hash(constraint_key)
	
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
		print(f"execution_mode: {self.execution_mode}")
		
		if self.execution_mode == 'concolic':
			return self._concolic_explore(max_iterations, dump_constraints, dump_trace, dump_semantics)
		elif self.execution_mode == 'concrete':
			return self._concrete_explore(max_iterations, dump_constraints, dump_trace, dump_semantics)
		else:  # symbolic
			return self._symbolic_explore(max_iterations, dump_constraints, dump_trace, dump_semantics)
		
	def _symbolic_explore(self, max_iterations=0, dump_constraints=False, dump_trace=False, dump_semantics=False):
		"""Symbolic execution mode"""
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
		
	def _concolic_explore(self, max_iterations=0, dump_constraints=False, dump_trace=False, dump_semantics=False):
		"""Concolic execution mode"""
		print("Starting concolic exploration...")
		
		# 生成初始具体值
		self._generate_concrete_values()
		
		# 执行具体执行
		self._oneExecution()
		print("First concrete execution completed")
		
		iterations = 1
		if max_iterations != 0 and iterations >= max_iterations:
			log.debug("Maximum number of iterations reached, terminating")
			if dump_constraints or dump_trace or dump_semantics:
				self._export_results()
			print("Returning early due to max iterations")
			return self.generated_inputs, self.execution_return_values, self.path

		# 进行concolic执行迭代
		concolic_iterations = min(self.concolic_iterations, max_iterations) if max_iterations > 0 else self.concolic_iterations
		
		for i in range(concolic_iterations):
			print(f"Concolic iteration {i+1}/{concolic_iterations}")
			
			if not self._isExplorationComplete():
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
			else:
				break

		if dump_constraints or dump_trace or dump_semantics:
			self._export_results()
		return self.generated_inputs, self.execution_return_values, self.path
		
	def _concrete_explore(self, max_iterations=0, dump_constraints=False, dump_trace=False, dump_semantics=False):
		"""Concrete execution mode"""
		print("Starting concrete exploration...")
		
		# 生成具体值
		self._generate_concrete_values()
		
		# 执行一次具体执行
		self._oneExecution()
		print("Concrete execution completed")
		
		if dump_constraints or dump_trace or dump_semantics:
			self._export_results()
		return self.generated_inputs, self.execution_return_values, self.path
		
	def _generate_concrete_values(self):
		"""Generate concrete values for symbolic inputs"""
		if hasattr(self.invocation, 'getNames'):
			for n in self.invocation.getNames():
				# 根据策略生成具体值
				if self.concrete_value_strategy == 'random':
					# 生成随机具体值
					concrete_value = self._generate_random_value(n)
				elif self.concrete_value_strategy == 'guided':
					# 生成引导性具体值
					concrete_value = self._generate_guided_value(n)
				else:  # hybrid
					# 生成混合策略的具体值
					concrete_value = self._generate_hybrid_value(n)
				
				# 更新符号输入为具体值
				self.symbolic_inputs[n] = concrete_value
		
	def _generate_random_value(self, name):
		"""Generate a random concrete value for a parameter"""
		# 实现真正的随机值生成，根据参数类型生成不同范围的随机值
		import random
		
		# 获取参数的默认值，以确定参数类型
		default_value = self.invocation.initial_value.get(name, 0)
		
		if isinstance(default_value, int):
			# 生成不同范围的随机整数
			random_value = random.choice([-100, -10, -1, 0, 1, 10, 100])
		elif isinstance(default_value, float):
			# 生成不同范围的随机浮点数
			random_value = random.choice([-100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0])
		elif isinstance(default_value, str):
			# 生成不同长度和内容的随机字符串
			random_strings = ["", "a", "ab", "abc", "abcd", "abcde"]
			random_value = random.choice(random_strings)
		elif isinstance(default_value, bool):
			# 生成随机布尔值
			random_value = random.choice([True, False])
		else:
			# 对于其他类型，使用默认值
			random_value = default_value
		
		return self.invocation.createArgumentValue(name, random_value)
		
	def _generate_guided_value(self, name):
		"""Generate a guided concrete value for a parameter"""
		# 实现基于程序控制流的引导性值生成
		# 考虑参数名称和类型，生成能够触发不同分支的具体值
		
		# 获取参数的默认值，以确定参数类型
		default_value = self.invocation.initial_value.get(name, 0)
		
		if isinstance(default_value, int):
			# 生成能够触发不同分支的整数值
			# 包括边界值和特殊值
			guided_values = [-100, -10, -1, 0, 1, 10, 100]
			# 根据参数名称选择可能的引导值
			if name.lower() in ['x', 'y', 'z']:
				# 对于常见的参数名，生成更有针对性的值
				return self.invocation.createArgumentValue(name, 10)  # 正数
			elif name.lower() in ['n', 'count', 'length']:
				# 对于计数或长度参数，生成非负整数
				return self.invocation.createArgumentValue(name, 5)
			else:
				# 对于其他参数，随机选择一个引导值
				import random
				return self.invocation.createArgumentValue(name, random.choice(guided_values))
		elif isinstance(default_value, float):
			# 生成能够触发不同分支的浮点数值
			guided_values = [-100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0]
			import random
			return self.invocation.createArgumentValue(name, random.choice(guided_values))
		elif isinstance(default_value, str):
			# 生成能够触发不同分支的字符串值
			guided_values = ["", "a", "ab", "abc", "test", "example"]
			import random
			return self.invocation.createArgumentValue(name, random.choice(guided_values))
		elif isinstance(default_value, bool):
			# 生成布尔值，优先选择True
			return self.invocation.createArgumentValue(name, True)
		else:
			# 对于其他类型，使用默认值
			return self.invocation.createArgumentValue(name)
		
	def _generate_hybrid_value(self, name):
		"""Generate a hybrid concrete value for a parameter"""
		# 实现混合策略，结合random和guided策略的优点
		import random
		
		# 70%的概率使用guided策略，30%的概率使用random策略
		if random.random() < 0.7:
			return self._generate_guided_value(name)
		else:
			return self._generate_random_value(name)
		
	def _track_code_coverage(self):
		"""跟踪代码覆盖率
		
		记录执行的代码行和分支，计算覆盖率统计指标
		"""
		# 获取当前路径的谓词
		current_path = self.path.get_current_path()
		
		# 跟踪执行的代码行
		for predicate in current_path:
			if predicate.source_file and predicate.source_line:
				# 记录执行的代码行
				line_key = f"{predicate.source_file}:{predicate.source_line}"
				self.code_coverage.add(line_key)
		
		# 可以添加更多覆盖率统计逻辑
		# 例如：分支覆盖率、函数覆盖率等
		
		# 计算覆盖率指标
		# 这里可以添加更复杂的覆盖率计算逻辑
		# 例如：与源代码行数比较，计算覆盖率百分比

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
			'path_lengths': self.path_lengths_list,
			'code_coverage': {
				'covered_lines': len(self.code_coverage),
				'covered_lines_list': list(self.code_coverage)
			}
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
		else:
			# If frontier is empty, export current path constraints
			current_path = self.path.get_current_path()
			if current_path:
				# Create a simple constraint from current path
				from .constraint import Constraint
				constraint = Constraint(None, None)
				for predicate in current_path:
					constraint = constraint.addChild(predicate)
				asserts, query = constraint.getAssertsAndQuery()
				self.smt_exporter.export_path(self.solver, asserts, query)
		
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
		
		try:
			if hasattr(self.invocation, 'callFunction'):
				ret = self.invocation.callFunction(self.symbolic_inputs)
			elif hasattr(self.invocation, 'execute'):
				ret = self.invocation.execute(self.symbolic_inputs)
			else:
				raise Exception("Unknown invocation type")
		except ZeroDivisionError as e:
			# 处理除零错误，记录为特殊返回值
			ret = "Division by zero"
		except Exception as e:
			# 处理其他异常，记录异常信息
			ret = str(e)
		print(ret)
		self.execution_return_values.append(ret)
		
		# 记录当前路径的长度和分支跟踪
		current_path = self.path.get_current_path()
		self.path_lengths_list.append(len(current_path))
		self.branch_traces_list.append(current_path.copy())
		
		# 记录已探索的路径
		if current_path:
			path_key = "|".join([str(trace) for trace in current_path])
			self.explored_paths.add(path_key)
		
		# 跟踪代码覆盖率（简单实现）
		# 这里可以添加更复杂的代码覆盖率跟踪逻辑
		self._track_code_coverage()

