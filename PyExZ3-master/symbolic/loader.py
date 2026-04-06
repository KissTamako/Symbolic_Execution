# Copyright: copyright.txt

import inspect
import re
import os
import sys
import types
from .invocation import FunctionInvocation
from .symbolic_types import SymbolicInteger, getSymbolic
from .ast_upcaster import transform_source_code

# The built-in definition of len wraps the return value in an int() constructor, destroying any symbolic types.
# By redefining len here we can preserve symbolic integer types.
import builtins
builtins.len = (lambda x : x.__len__())

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
		# Use inspect.signature for Python 3.11+ compatibility
		try:
			# Try getargspec for older Python versions
			argspec = inspect.getargspec(func)
			arg_names = argspec.args
		except AttributeError:
			# Fall back to inspect.signature for Python 3.11+
			sig = inspect.signature(func)
			arg_names = list(sig.parameters.keys())
		
		# check to see if user specified initial values of arguments
		if "concrete_args" in func.__dict__:
			for (f,v) in func.concrete_args.items():
				if not f in arg_names:
					print("Error in @concrete: " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				else:
					Loader._initializeArgumentConcrete(inv,f,v)
		if "symbolic_args" in func.__dict__:
			for (f,v) in func.symbolic_args.items():
				if not f in arg_names:
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
		for a in arg_names:
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
			return self._check(return_vals, self.app.__dict__["expected_result"]())
		if "expected_result_set" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result_set"](),False)
		else:
			print(self._fileName + ".py contains no expected_result function")
			return None

	# -- private

	def _resetCallback(self,firstpass=False):
		self.app = None
		if firstpass and self._fileName in sys.modules:
			print("There already is a module loaded named " + self._fileName)
			raise ImportError()
		try:
			if (not firstpass and self._fileName in sys.modules):
				del(sys.modules[self._fileName])
			
			# 获取文件完整路径
			# 首先尝试从sys.path中查找文件
			file_path = None
			for path_dir in sys.path:
				possible_path = os.path.join(path_dir, f"{self._fileName}.py")
				if os.path.exists(possible_path):
					file_path = possible_path
					break
			
			# 如果没找到，使用当前工作目录
			if file_path is None:
				file_path = os.path.join(os.getcwd(), f"{self._fileName}.py")
			
			# 读取源文件内容（处理编码问题）
			# 先尝试UTF-8，如果失败则尝试系统默认编码
			source_code = None
			encodings_to_try = ['utf-8', 'utf-8-sig', 'gbk', 'cp936', 'latin-1']
			
			for encoding in encodings_to_try:
				try:
					with open(file_path, 'r', encoding=encoding) as f:
						source_code = f.read()
					break
				except UnicodeDecodeError:
					continue
			
			if source_code is None:
				# 如果所有编码都失败，使用二进制读取
				with open(file_path, 'rb') as f:
					binary_content = f.read()
				# 尝试UTF-8解码，忽略错误
				source_code = binary_content.decode('utf-8', errors='ignore')
			
			# AST转换（常量提升）- 默认启用
			transformed_source, code_obj = transform_source_code(source_code, enable_upcasting=True)
			
			# 创建模块对象
			module = types.ModuleType(self._fileName)
			
			# 注入符号类型类到模块命名空间，避免AST转换后代码出现NameError
			# AST转换器生成的代码需要使用这些符号类型类
			# 确保即使某些类导入失败，也能提供基本的占位类
			symbolic_classes = {}
			
			# 尝试导入每个符号类，如果失败则创建简单的占位类
			class_imports = [
				('SymbolicInteger', 'symbolic.symbolic_types.symbolic_int'),
				('SymbolicStr', 'symbolic.symbolic_types.symbolic_str'),
				('SymbolicFloat', 'symbolic.symbolic_types.symbolic_float'),
				('SymbolicRange', 'symbolic.symbolic_types.symbolic_range'),
				('SymbolicDict', 'symbolic.symbolic_types.symbolic_dict'),
				('SymbolicList', 'symbolic.symbolic_types.symbolic_list'),
			]
			
			for class_name, module_path in class_imports:
				try:
					# 动态导入类
					module_parts = module_path.split('.')
					import_module = __import__(module_path)
					for part in module_parts[1:]:
						import_module = getattr(import_module, part)
					
					# 获取类
					class_obj = getattr(import_module, class_name)
					symbolic_classes[class_name] = class_obj
					
				except Exception as e:
					# 创建简单的占位类，防止NameError
					print(f"[警告] 无法导入{class_name}: {e}，创建占位类")
					
					# 创建简单的占位类
					class PlaceholderClass:
						def __init__(self, name, value, expr=None):
							self.name = name
							self.value = value
							self.expr = expr
							self.val = value
						
						def getConcrValue(self):
							return self.value
						
						def isVariable(self):
							return True
						
						def __repr__(self):
							return f"{class_name}({self.name!r}, {self.value!r})"
					
					symbolic_classes[class_name] = PlaceholderClass
			
			# 将符号类型类注入到模块命名空间
			# 注意：避免覆盖用户已有的定义
			for class_name, class_obj in symbolic_classes.items():
				if class_name not in module.__dict__:
					module.__dict__[class_name] = class_obj
					
			print(f"[调试] 已注入符号类: {list(symbolic_classes.keys())}")
			
			# 执行转换后的代码
			exec(code_obj, module.__dict__)
			
			# 注册模块
			sys.modules[self._fileName] = module
			self.app = module
			
			if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
				print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
				raise ImportError()
				
		except Exception as arg:
			print("Couldn't import " + self._fileName)
			print(arg)
			raise ImportError()

	def _execute(self, **args):
		return self.app.__dict__[self._entryPoint](**args)

	def _toBag(self,l):
		bag = {}
		for i in l:
			if i in bag:
				bag[i] += 1
			else:
				bag[i] = 1
		return bag

	def _check(self, computed, expected, as_bag=True):
		b_c = self._toBag(computed)
		b_e = self._toBag(expected)
		if as_bag and b_c != b_e or not as_bag and set(computed) != set(expected):
			print("-------------------> %s test failed <---------------------" % self._fileName)
			print("Expected: %s, found: %s" % (b_e, b_c))
			return False
		else:
			print("%s test passed <---" % self._fileName)
			return True
	
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


