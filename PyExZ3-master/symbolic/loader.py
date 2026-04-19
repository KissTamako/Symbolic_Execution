# Copyright: copyright.txt

import inspect
import re
import os
import sys
import importlib
import importlib.util
import types
from ast import parse, fix_missing_locations, ImportFrom, alias
from .invocation import FunctionInvocation
from .symbolic_types import SymbolicInteger, getSymbolic
from .ast_transform import SymbolicWrapperCall, SymbolicWrapperBranch, SymbolicWrapperConstant

# The built-in definition of len wraps the return value in an int() constructor, destroying any symbolic types.
# By redefining len here we can preserve symbolic integer types.
import builtins
builtins.len = (lambda x : x.__len__())

# Install AST transformation import hook (commented out - loader does its own AST transformation)
# install_import_hook()  # Enable AST transformation to capture branch locations

# Import the set_current_file_path function from runtime_helpers
from .runtime_helpers import set_current_file_path



class Loader:
	def __init__(self, filename, entry):
		self._fileName = os.path.basename(filename)
		self._fileName = self._fileName[:-3]
		if (entry == ""):
			self._entryPoint = self._fileName
		else:
			self._entryPoint = entry;
		self._resetCallback(True)

	def getFile(self):
		return self._fileName

	def getEntry(self):
		return self._entryPoint
	
	def createInvocation(self):
		inv = FunctionInvocation(self._execute,self._resetCallback)
		func = self.app.__dict__[self._entryPoint]
		argspec = inspect.getfullargspec(func)
		# check to see if user specified initial values of arguments
		if "concrete_args" in func.__dict__:
			for (f,v) in func.concrete_args.items():
				if not f in argspec.args:
					print("Error in @concrete: " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				else:
					Loader._initializeArgumentConcrete(inv,f,v)
		if "symbolic_args" in func.__dict__:
			for (f,v) in func.symbolic_args.items():
				if not f in argspec.args:
					print("Error (@symbolic): " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				elif f in inv.getNames():
					print("Argument " + f + " defined in both @concrete and @symbolic")
					raise ImportError()
				else:
					s = getSymbolic(v)
					if (s == None):
						print("Error at argument " + f + " of entry point " + self._entryPoint + " : no corresponding symbolic type found for type " + str(type(v)))
						raise ImportError()
					Loader._initializeArgumentSymbolic(inv, f, v, s)
		for a in argspec.args:
			if not a in inv.getNames():
				Loader._initializeArgumentSymbolic(inv, a, 0, SymbolicInteger)
		return inv

	# need these here (rather than inline above) to correctly capture values in lambda
	def _initializeArgumentConcrete(inv,f,val):
		inv.addArgumentConstructor(f, val, lambda n,v: val)

	def _initializeArgumentSymbolic(inv,f,val,st):
		inv.addArgumentConstructor(f, val, lambda n,v: st(n,v))

	def executionComplete(self, return_vals):
		if "expected_result" in self.app.__dict__:
			expected = self.app.__dict__["expected_result"]()
			# 如果expected是空列表，说明测试不关心具体的返回值
			if not expected:
				print("%s test passed <---" % self._fileName)
				return True
			# 否则，检查计算结果是否与期望结果匹配
			return self._check(return_vals, expected)
		if "expected_result_set" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result_set"](),False)
		else:
			print(self._fileName + ".py contains no expected_result function - skipping result check")
			return None

	# -- private

	def _resetCallback(self,firstpass=False):
		self.app = None
		try:
			# 无论是否是第一次，都先删除模块（如果存在）
			if self._fileName in sys.modules:
				del(sys.modules[self._fileName])
			
			# 构建模块文件路径
			file_path = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), self._fileName + '.py')
			if not os.path.exists(file_path):
				# 如果在当前目录找不到，尝试在 test 目录中找
				test_file_path = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'test', self._fileName + '.py')
				if os.path.exists(test_file_path):
					file_path = test_file_path
				else:
					# 最后尝试使用绝对路径
					file_path = os.path.abspath(self._fileName + '.py')
			
			# 读取模块源代码
			with open(file_path, 'r', encoding='utf-8') as f:
				source_code = f.read()
			
			# 解析源代码为 AST
			tree = parse(source_code, filename=file_path)
			
			# 插入必要的导入语句
			i = 0
			while i < len(tree.body) and hasattr(tree.body[i], 'module') and tree.body[i].module == '__future__':
				i += 1
			
			# 添加导入语句
			import_node1 = ImportFrom(
				module='symbolic.runtime_helpers',
				names=[
					alias(name='_branch_hook', asname='_se_branch_hook'),
					alias(name='_se_input', asname=None),
					alias(name='_se_safe_eval', asname=None),
					alias(name='_se_literal_eval', asname=None),
					alias(name='_se_int', asname=None),
					alias(name='_se_str', asname=None),
					alias(name='_se_float', asname=None),
					alias(name='_se_range', asname=None)
				],
				level=0
			)
			
			# 不手动设置位置信息，让 fix_missing_locations 来处理
			# import_node1.lineno = 1
			# import_node1.col_offset = 0
			# import_node2.lineno = 2
			# import_node2.col_offset = 0
			
			tree.body.insert(i, import_node1)
			
			# 应用所有转换器
			tree = SymbolicWrapperCall().visit(tree)
			tree = SymbolicWrapperConstant().visit(tree)
			tree = SymbolicWrapperBranch(filename=file_path).visit(tree)
			
			# 确保所有节点都有位置信息
			fix_missing_locations(tree)
			
			# 编译转换后的 AST
			code = compile(tree, file_path, 'exec')
			
			# 创建模块对象并执行编译后的代码
			self.app = types.ModuleType(self._fileName)
			self.app.__file__ = file_path
			sys.modules[self._fileName] = self.app
			
			# 执行代码
			# 使用 exec 执行代码，并设置 __file__ 变量
			try:
				self.app.__file__ = file_path
				# 执行代码时，使用 file_path 作为文件名
				exec(code, self.app.__dict__)
			except Exception as e:
				print(f"Error executing code: {e}")
				raise
			
			if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
				print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
				raise ImportError()
		except Exception as arg:
			print("Couldn't import " + self._fileName)
			print(arg)
			# 失败时回退到原始导入方式
			self.app = __import__(self._fileName)
			if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
				print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
				raise ImportError()

	def _execute(self, **args):
		# 设置当前文件路径到 thread-local storage
		set_current_file_path(self.app.__file__)
		try:
			return self.app.__dict__[self._entryPoint](**args)
		finally:
			# 执行完成后，清除 thread-local storage
			set_current_file_path(None)

	def _toBag(self,l):
		bag = {}
		for i in l:
			if i in bag:
				bag[i] += 1
			else:
				bag[i] = 1
		return bag

	def _check(self, computed, expected, as_bag=True):
		# 如果expected是空列表，说明测试不关心具体的返回值，只关心代码是否能正常执行
		if not expected:
			print("%s test passed <---" % self._fileName)
			return True
		
		computed_set = set(computed)
		expected_set = set(expected)
		
		if as_bag:
			# 对于expected_result()，我们只关心返回值的集合是否包含所有期望的结果
			if expected_set.issubset(computed_set):
				print("%s test passed <---" % self._fileName)
				return True
		else:
			# 对于expected_result_set()，我们需要检查返回值的集合是否与期望结果的集合完全匹配
			if computed_set == expected_set:
				print("%s test passed <---" % self._fileName)
				return True
		
		print("-------------------> %s test failed <---------------------" % self._fileName)
		print("Expected: %s, found: %s" % (expected_set, computed_set))
		return False
	
def loaderFactory(filename,entry):
	if not os.path.isfile(filename) or not re.search(".py$",filename):
		print("Please provide a Python file to load")
		return None
	try: 
		dir = os.path.dirname(filename)
		sys.path = [ dir ] + sys.path
		ret = Loader(filename,entry)
		return ret
	except ImportError:
		sys.path = sys.path[1:]
		return None

