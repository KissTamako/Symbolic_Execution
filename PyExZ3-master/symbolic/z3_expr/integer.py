from z3 import *
from .expression import Z3Expression

class Z3Integer(Z3Expression):
	def _isIntVar(self,v):
		# Check if v is an arithmetic reference (integer variable in Z3)
		return isinstance(v,ArithRef)

	def _variable(self,name,solver):
		return Int(name,solver.ctx)

	def _constant(self,v,solver):
		return IntVal(v,solver.ctx)
	
	def _string_constant(self, s, solver):
		"""Convert a Python string to a Z3 string constant.
		Note: Z3's string support may require appropriate theories."""
		try:
			# Try to create a Z3 string constant
			# StringVal is available in Z3 4.8+ with string theory
			# Note: StringVal returns a SeqRef (string) in Z3
			return StringVal(s)
		except Exception as e:
			# Fallback: treat strings as integer representation (not ideal)
			# This is a temporary workaround until proper string support is implemented
			# We'll use a hash of the string as an integer representation
			import hashlib
			hash_val = int(hashlib.md5(s.encode()).hexdigest()[:8], 16) % (2**31)
			return IntVal(hash_val, solver.ctx)

	def _abs(self, v, solver):
		# Absolute value: if v >= 0 then v else -v
		return If(v >= 0, v, -v)
	
	def _neg(self, v, solver):
		# Negation: -v
		return -v
	
	def _floordiv(self, l, r, solver):
		"""Integer floor division (//). In Z3, integer division is floor division."""
		# Z3's integer division operator '/' performs floor division for integers
		return l / r
	
	def _truediv(self, l, r, solver):
		"""True division (/). Converts integers to real numbers for division."""
		# Convert integers to real numbers for true division
		# Only convert if they are integers, otherwise keep as is
		try:
			l_real = ToReal(l)
		except Exception:
			# l is already a real number
			l_real = l
		
		try:
			r_real = ToReal(r)
		except Exception:
			# r is already a real number
			r_real = r
		
		return l_real / r_real
	
	def _mod(self, l, r, solver):
		# Integer modulo operation
		return l % r

	def _lsh(self, l, r, solver):
		# Left shift for integers (only works when r is concrete)
		# For symbolic r, we need to handle differently
		# Using Z3's built-in shift left for bitvectors, but for integers we use multiplication
		return l * (2 ** r)

	def _rsh(self, l, r, solver):
		# Right shift for integers (only works when r is concrete)
		# Using division by power of 2
		return l / (2 ** r)

	def _xor(self, l, r, solver):
		# Bitwise XOR for integers - use Z3's bitwise XOR
		return l ^ r

	def _or(self, l, r, solver):
		# Bitwise OR for integers
		return l | r

	def _and(self, l, r, solver):
		# Bitwise AND for integers
		return l & r
	
	def _pow(self, l, r, solver):
		"""Power operation (l ** r). For integer powers, we use multiplication.
		Note: This only supports integer exponents. For symbolic exponents,
		we need more complex handling."""
		# For concrete small exponents, we can use repeated multiplication
		# For symbolic exponents or large concrete exponents, this is complex
		# We'll provide a basic implementation for small concrete exponents
		try:
			# Try to evaluate r concretely
			if isinstance(r, int) or (hasattr(r, 'as_long') and callable(getattr(r, 'as_long'))):
				exp_val = r if isinstance(r, int) else r.as_long()
				if exp_val >= 0 and exp_val <= 10:  # Limit to reasonable exponents
					result = l
					for _ in range(1, exp_val):
						result = result * l
					if exp_val == 0:
						result = self._constant(1, solver)
					return result
		except:
			pass
		
		# Fallback: use Z3's power function if available, or create a function
		# Note: Z3 doesn't have a built-in power function for integers
		# For now, we'll create a function declaration
		pow_fun = Function('int_pow', IntSort(), IntSort(), IntSort())
		return pow_fun(l, r)
	
	# String operation methods
	def _str_len(self, s, solver):
		"""String length operation - str.len"""
		try:
			# Use Z3's Length function for strings
			return Length(s)
		except Exception as e:
			# Fallback: check if s is a concrete string
			if isinstance(s, str):
				return self._constant(len(s), solver)
			# Fallback 2: check if s is a Z3 expression that might be a string
			try:
				# Try to get string value from Z3 model if possible
				# If s is a Z3 expression, we can't determine length symbolically
				# Return a symbolic integer variable for length
				from z3 import Int, IntSort
				# Create a fresh integer variable for string length
				length_var = Int(f"str_len_{len(self.z3_vars)}")
				return length_var
			except Exception as inner_e:
				# Ultimate fallback: return 0 as placeholder
				return self._constant(0, solver)
	
	def _str_isalpha(self, s, solver):
		"""String isalpha check - str.isalpha
		
		Z3不支持字符类别检查函数（如IsAlpha）。
		返回符号化布尔变量允许符号执行探索True/False两种可能性。
		"""
		return FreshBool()
	
	def _str_isdigit(self, s, solver):
		"""String isdigit check - str.isdigit
		
		Z3不支持字符类别检查函数（如IsDigit）。
		返回符号化布尔变量允许符号执行探索True/False两种可能性。
		"""
		return FreshBool()
	
	def _str_islower(self, s, solver):
		"""String islower check - str.islower
		
		Z3不支持字符大小写检查函数。
		返回符号化布尔变量允许符号执行探索True/False两种可能性。
		"""
		return FreshBool()
	
	def _str_isupper(self, s, solver):
		"""String isupper check - str.isupper
		
		Z3不支持字符大小写检查函数。
		返回符号化布尔变量允许符号执行探索True/False两种可能性。
		"""
		return FreshBool()
	
	def _str_upper(self, s, solver):
		"""String upper case conversion - str.upper"""
		# Return a fresh string variable representing the transformed string
		# This allows symbolic execution to explore different transformations
		# Create a new string variable with a unique name
		import uuid
		var_name = f"upper_{uuid.uuid4().hex[:8]}"
		return String(var_name)
	
	def _str_lower(self, s, solver):
		"""String lower case conversion - str.lower"""
		# Return a fresh string variable representing the transformed string
		# Create a new string variable with a unique name
		import uuid
		var_name = f"lower_{uuid.uuid4().hex[:8]}"
		return String(var_name)
	
	def _str_concat(self, s1, s2, solver):
		"""String concatenation - str1 + str2
		
		Z3支持Concat函数进行字符串拼接。
		如果s1或s2是字符串常量，使用StringVal转换。
		"""
		try:
			# 将第一个字符串转换为Z3字符串表达式
			if isinstance(s1, str):
				s1_expr = StringVal(s1)
			else:
				s1_expr = s1
				
			# 将第二个字符串转换为Z3字符串表达式
			if isinstance(s2, str):
				s2_expr = StringVal(s2)
			else:
				s2_expr = s2
				
			# 使用Z3的Concat函数
			# Concat(字符串1, 字符串2) 返回拼接后的字符串
			return Concat(s1_expr, s2_expr)
		except Exception as e:
			# 如果Z3不支持或出错，返回新的字符串变量作为回退
			import uuid
			var_name = f"concat_{uuid.uuid4().hex[:8]}"
			return String(var_name)
	
	def _str_endswith(self, s, suffix, solver):
		"""String endswith check - str.endswith
		
		Z3支持SuffixOf函数检查后缀关系。
		如果suffix是字符串常量，使用StringVal转换。
		"""
		try:
			# 将后缀转换为Z3字符串表达式（如果是Python字符串）
			if isinstance(suffix, str):
				suffix_expr = StringVal(suffix)
			else:
				suffix_expr = suffix
				
			# 使用Z3的SuffixOf函数
			return SuffixOf(s, suffix_expr)
		except Exception as e:
			# 如果Z3不支持或出错，返回符号布尔变量作为回退
			# 这允许符号执行探索两种可能性
			return FreshBool()
	
	def _str_startswith(self, s, prefix, solver):
		"""String startswith check - str.startswith
		
		Z3支持PrefixOf函数检查前缀关系。
		如果prefix是字符串常量，使用StringVal转换。
		"""
		try:
			# 将前缀转换为Z3字符串表达式（如果是Python字符串）
			if isinstance(prefix, str):
				prefix_expr = StringVal(prefix)
			else:
				prefix_expr = prefix
				
			# 使用Z3的PrefixOf函数
			return PrefixOf(s, prefix_expr)
		except Exception as e:
			# 如果Z3不支持或出错，返回符号布尔变量作为回退
			# 这允许符号执行探索两种可能性
			return FreshBool()
	
	def _str_find(self, s, sub, solver, beg=0):
		"""String find operation - str.find
		
		Z3支持IndexOf函数查找子串位置。
		返回-1如果未找到，否则返回子串起始位置。
		"""
		try:
			# 将子串转换为Z3字符串表达式（如果是Python字符串）
			if isinstance(sub, str):
				sub_expr = StringVal(sub)
			else:
				sub_expr = sub
				
			# 使用Z3的IndexOf函数，支持起始位置参数
			# IndexOf返回子串在字符串中的起始位置，如果未找到则返回-1
			# 这与Python的str.find()行为一致
			index_result = IndexOf(s, sub_expr, beg)
			return index_result
		except Exception as e:
			# 如果Z3不支持或出错，返回符号整数变量作为回退
			# 这允许符号执行探索不同的位置
			return FreshInt()
	
	def _str_index(self, s, sub, solver, beg=0, end=None):
		"""String index operation - str.index
		
		Z3支持IndexOf函数查找子串位置。
		注意：Python的str.index()在未找到时引发ValueError，
		但Z3的IndexOf返回-1表示未找到。
		在符号执行中，我们需要在约束求解阶段处理这个差异。
		"""
		try:
			# 将子串转换为Z3字符串表达式（如果是Python字符串）
			if isinstance(sub, str):
				sub_expr = StringVal(sub)
			else:
				sub_expr = sub
				
			# 使用Z3的IndexOf函数
			# 注意：IndexOf返回-1如果未找到，而str.index()会引发异常
			# 在符号执行中，我们将返回-1视为未找到的情况
			index_result = IndexOf(s, sub_expr, beg)
			return index_result
		except Exception as e:
			# 如果Z3不支持或出错，返回符号整数变量作为回退
			return FreshInt()
	
	def _str_isalnum(self, s, solver):
		"""String isalnum check - str.isalnum"""
		# Return a fresh boolean variable for symbolic execution
		return FreshBool()
	
	def _str_isnumeric(self, s, solver):
		"""String isnumeric check - str.isnumeric"""
		# Return a fresh boolean variable for symbolic execution
		return FreshBool()
	
	def _str_strip(self, s, solver):
		"""String strip operation - str.strip()"""
		# Return a fresh string variable representing the stripped string
		# This allows symbolic execution to explore different transformations
		import uuid
		var_name = f"strip_{uuid.uuid4().hex[:8]}"
		return String(var_name)
	
	def _str_lstrip(self, s, solver):
		"""String lstrip operation - str.lstrip()"""
		# Return a fresh string variable representing the left-stripped string
		import uuid
		var_name = f"lstrip_{uuid.uuid4().hex[:8]}"
		return String(var_name)
	
	def _str_rstrip(self, s, solver):
		"""String rstrip operation - str.rstrip()"""
		# Return a fresh string variable representing the right-stripped string
		import uuid
		var_name = f"rstrip_{uuid.uuid4().hex[:8]}"
		return String(var_name)
	
	def _str_split(self, s, solver, sep=None):
		"""String split operation - str.split()"""
		# Return a fresh string variable representing the split result
		# For simplicity, return a string representing the split operation
		# In a complete implementation, this would return a list
		import uuid
		var_name = f"split_{uuid.uuid4().hex[:8]}"
		return String(var_name)
	
	def _str_replace(self, s, old, new, solver):
		"""String replace operation - str.replace()
		
		Z3支持Replace函数进行字符串替换。
		如果old或new是字符串常量，使用StringVal转换。
		"""
		try:
			# 将旧字符串转换为Z3字符串表达式
			if isinstance(old, str):
				old_expr = StringVal(old)
			else:
				old_expr = old
				
			# 将新字符串转换为Z3字符串表达式
			if isinstance(new, str):
				new_expr = StringVal(new)
			else:
				new_expr = new
				
			# 使用Z3的Replace函数
			# Replace(字符串, 旧子串, 新子串) 返回替换后的字符串
			return Replace(s, old_expr, new_expr)
		except Exception as e:
			# 如果Z3不支持或出错，返回新的字符串变量作为回退
			import uuid
			var_name = f"replace_{uuid.uuid4().hex[:8]}"
			return String(var_name)
	
	def _float_constant(self, v, solver):
		"""Convert a Python float to a Z3 Real constant."""
		try:
			# Create a Z3 Real constant
			# RealVal creates a real number constant in Z3
			return RealVal(v, solver.ctx)
		except Exception as e:
			# Fallback: try alternative methods to create Real value
			# First try using RealVal with string representation
			try:
				return RealVal(str(v), solver.ctx)
			except Exception as e2:
				# If that fails, create a Real variable with the float value
				try:
					# Create a Real variable initialized with the float value
					return Real(str(v), solver.ctx)
				except Exception as e3:
					# Last resort: create a symbolic Real variable
					# Use a fresh name based on the float value
					import uuid
					var_name = f"float_const_{abs(hash(v))}_{uuid.uuid4().hex[:8]}"
					return Real(var_name, solver.ctx)
	
	def _getFloatVariable(self, name, solver):
		"""Get or create a Z3 Real variable for a float symbolic variable.
		
		这个方法应该在_astToZ3Expr方法中被调用，当遇到SymbolicFloat变量时。
		但当前的设计中，_getIntegerVariable只处理整数变量，所以我们需要一个新的方法。
		"""
		# TODO: 在z3_expr/expression.py中添加调用此方法的分支
		if name not in self.z3_vars:
			# 创建Z3 Real变量
			self.z3_vars[name] = Real(name, solver.ctx)
		return self.z3_vars[name]
	
	def _create_float_variable(self, name, solver):
		"""创建Z3 Real变量（与_getFloatVariable相同，但更具描述性）"""
		return self._getFloatVariable(name, solver)
	
	def _getRangeVariable(self, name, solver):
		"""Get or create a Z3 representation for a range symbolic variable.
		
		Returns a tuple (start, stop, step) as symbolic integers.
		We'll return start as the representative value for now.
		"""
		try:
			# For ranges, we need three variables: start, stop, step
			# We'll create them with suffixes
			start_name = f"{name}_start"
			stop_name = f"{name}_stop"
			step_name = f"{name}_step"
			
			if start_name not in self.z3_vars:
				self.z3_vars[start_name] = Int(start_name, solver.ctx)
				self.z3_vars[stop_name] = Int(stop_name, solver.ctx)
				self.z3_vars[step_name] = Int(step_name, solver.ctx)
			
			# Return start as representative value
			return self.z3_vars[start_name]
		except Exception as e:
			# Fallback to constant 0
			return self._constant(0, solver)
	
	def _range_constant(self, v, solver):
		"""Convert a Python range to a Z3 Seq representation.
		
		Z3 has Seq theory for sequences. We'll represent range as an integer sequence.
		For range(start, stop, step), we create a symbolic sequence where
		element i = start + i * step, for i in [0, len(range)-1]
		"""
		try:
			if not isinstance(v, range):
				# Not a range, fallback to constant 0
				return self._constant(0, solver)
			
			# For Z3 Seq theory, we can represent range as constraints
			# rather than an explicit sequence. We'll return a tuple:
			# (start, stop, step) as integer values
			start = self._constant(v.start, solver) if hasattr(v, 'start') else self._constant(0, solver)
			stop = self._constant(v.stop, solver) if hasattr(v, 'stop') else self._constant(0, solver)
			step = self._constant(v.step, solver) if hasattr(v, 'step') else self._constant(1, solver)
			
			# We'll return start as a placeholder for now
			# In a more complete implementation, we would create a sequence
			return start
		except Exception as e:
			# Fallback: return 0
			return self._constant(0, solver)
	
	def _list_constant(self, v, solver):
		"""Convert a Python list to a Z3 Array constant.
		
		Creates a Z3 array constant where indices map to list elements.
		For empty list, returns a default array.
		"""
		try:
			if not isinstance(v, list):
				# Not a list, create a default empty array
				array_sort = ArraySort(IntSort(), IntSort())
				return K(array_sort, IntVal(0, solver.ctx))
			
			if len(v) == 0:
				# Empty list: create default array (all indices map to 0)
				# ArraySort(IntSort(), IntSort()) creates an array from int to int
				array_sort = ArraySort(IntSort(), IntSort())
				return K(array_sort, IntVal(0, solver.ctx))
			
			# For non-empty list, create array with elements
			# We'll create an array and set each element individually
			# Start with default array (all indices map to 0)
			array_sort = ArraySort(IntSort(), IntSort())
			array_expr = K(array_sort, IntVal(0, solver.ctx))
			
			# Set each element at its index
			for i, elem in enumerate(v):
				# Convert element value to Z3 integer
				if isinstance(elem, (int, float)):
					if isinstance(elem, float):
						# For float elements, we need to handle as Real or convert to Int
						# Since this is integer.py, we'll convert to integer (floor)
						elem_val = IntVal(int(elem), solver.ctx)
					else:
						elem_val = IntVal(elem, solver.ctx)
					# Store in array: Store(array, index, value)
					array_expr = Store(array_expr, IntVal(i, solver.ctx), elem_val)
				else:
					# Non-numeric element, use 0
					array_expr = Store(array_expr, IntVal(i, solver.ctx), IntVal(0, solver.ctx))
			
			return array_expr
		except Exception as e:
			# Fallback: create a default empty array
			array_sort = ArraySort(IntSort(), IntSort())
			return K(array_sort, IntVal(0, solver.ctx))
	
	def _getListVariable(self, name, solver):
		"""Get or create a Z3 Array variable for a list symbolic variable.
		
		Creates an array variable of type Array(Int, Int) for integer lists.
		"""
		try:
			# Check if we already created this list variable
			if name not in self.z3_vars:
				# Create Z3 array variable: Array(Int, Int)
				array_sort = ArraySort(IntSort(), IntSort())
				self.z3_vars[name] = Const(name, array_sort)
			return self.z3_vars[name]
		except Exception as e:
			# Fallback to constant 0
			return self._constant(0, solver)
	
	def _range_len(self, r, solver):
		"""Get length of a range"""
		# Return a fresh integer variable for symbolic execution
		return FreshInt()
	
	def _range_contains(self, r, item, solver):
		"""Check if item is in range"""
		# Return a fresh boolean variable for symbolic execution
		return FreshBool()
	
	def _range_count(self, r, item, solver):
		"""Count occurrences of item in range (0 or 1)"""
		# Return a fresh integer variable for symbolic execution
		return FreshInt()
	
	def _range_index(self, r, item, solver):
		"""Get index of item in range, or -1 if not found"""
		# Return a fresh integer variable for symbolic execution
		return FreshInt()
	
	def _range_getitem(self, r, index, solver):
		"""Get item at index in range"""
		try:
			# For now, return the index itself as a placeholder
			return index
		except Exception as e:
			return self._constant(0, solver)
	
	def _dict_constant(self, v, solver):
		"""Convert a Python dict to a Z3 Map/Array representation.
		
		Creates a Z3 array constant where keys map to values.
		For empty dict, returns a default array.
		"""
		try:
			if not isinstance(v, dict):
				# Not a dict, fallback to constant 0
				return self._constant(0, solver)
			
			if len(v) == 0:
				# Empty dict: create default array (all keys map to 0)
				# ArraySort(IntSort(), IntSort()) creates an array from int to int
				array_sort = ArraySort(IntSort(), IntSort())
				return K(array_sort, IntVal(0, solver.ctx))
			
			# For non-empty dict, create array with key-value pairs
			# We'll create an array and set each key-value pair
			# Start with default array (all keys map to 0)
			array_sort = ArraySort(IntSort(), IntSort())
			array_expr = K(array_sort, IntVal(0, solver.ctx))
			
			# Set each key-value pair
			for key, value in v.items():
				# Convert key and value to Z3 integers
				if isinstance(key, (int, float)) and isinstance(value, (int, float)):
					key_val = IntVal(int(key), solver.ctx)
					val_val = IntVal(int(value), solver.ctx)
					# Store in array: Store(array, key, value)
					array_expr = Store(array_expr, key_val, val_val)
				else:
					# Non-integer key/value, skip for now
					pass
			
			return array_expr
		except Exception as e:
			# Fallback to constant 0
			return self._constant(0, solver)
	
	def _getDictVariable(self, name, solver):
		"""Get or create a Z3 Array variable for a dict symbolic variable.
		
		Creates an array variable of type Array(Int, Int) for integer dicts.
		"""
		try:
			# Check if we already created this dict variable
			if name not in self.z3_vars:
				# Create Z3 array variable: Array(Int, Int)
				array_sort = ArraySort(IntSort(), IntSort())
				self.z3_vars[name] = Const(name, array_sort)
			return self.z3_vars[name]
		except Exception as e:
			# Fallback to constant 0
			return self._constant(0, solver)
	
	# List operation implementations
	def _list_len(self, l, solver):
		"""List length operation - list.len"""
		# Return a fresh integer variable for symbolic execution
		return FreshInt()
	
	def _list_getitem(self, l, index, solver):
		"""List getitem operation - list.getitem"""
		try:
			# l is expected to be a Z3 array expression
			# Use Select to get element at index
			# Select(array, index) returns the value at index
			return Select(l, index)
		except Exception as e:
			# Fallback to index itself
			return index
	
	def _list_contains(self, l, item, solver):
		"""List contains operation - list.contains"""
		try:
			# For Z3 arrays, checking containment is complex
			# We would need to check if item exists at any index
			# For now, return symbolic boolean (unknown)
			# This creates a fresh boolean variable
			return FreshBool()
		except Exception as e:
			# Fallback to false
			return self._wrapIf(self._constant(1, solver) == self._constant(0, solver), solver, None)
	
	def _list_count(self, l, item, solver):
		"""List count operation - list.count"""
		try:
			# Counting occurrences in Z3 array is complex
			# For now, return symbolic integer (0 or positive)
			return FreshInt()
		except Exception as e:
			# Fallback to 0
			return self._constant(0, solver)
	
	def _list_index(self, l, item, solver, start=0, end=None):
		"""List index operation - list.index"""
		try:
			# Finding index in Z3 array is complex
			# For now, return symbolic integer (-1 if not found, else index)
			return FreshInt()
		except Exception as e:
			# Fallback to -1
			return self._constant(-1, solver)
	
	def _list_constructor(self, elements, solver):
		"""List constructor - create a list from elements"""
		try:
			# Create array from elements
			if len(elements) == 0:
				# Empty array
				array_sort = ArraySort(IntSort(), IntSort())
				return K(array_sort, IntVal(0, solver.ctx))
			
			# Create array and store each element
			array_sort = ArraySort(IntSort(), IntSort())
			array_expr = K(array_sort, IntVal(0, solver.ctx))
			
			for i, elem in enumerate(elements):
				array_expr = Store(array_expr, IntVal(i, solver.ctx), elem)
			
			return array_expr
		except Exception as e:
			# Fallback to first element if available
			if len(elements) > 0:
				return elements[0]
			return self._constant(0, solver)
