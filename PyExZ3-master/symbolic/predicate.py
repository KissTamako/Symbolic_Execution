# Copyright - see copyright.txt

class Predicate:
	"""Predicate is one specific ``if'' encountered during the program execution."""
	def __init__(self, st, result, source_file=None, source_line=None, branch_id=None):
		self.symtype = st
		self.result = result
		self.expr = st.toString() if hasattr(st, 'toString') else str(st)
		
		self.source_file = source_file
		self.source_line = source_line
		self.branch_id = branch_id
		# Extract variables, filtering out 'const' which is a placeholder for constants
		all_vars = st.getVars() if hasattr(st, 'getVars') else []
		self.vars = [v for v in all_vars if v != 'const']
		# Extract constants - 'const' represents concrete constant values
		self.constants = {}
		if 'const' in all_vars:
			# Try to extract the constant value from the expression
			const_value = self._extract_const_value(st)
			if const_value is not None:
				self.constants['const'] = const_value
		
		# Parse the string expression to tree structure (for PyCT compatibility)
		# Must be called after self.constants is initialized
		self.expr_tree = self._parse_to_tree(self.expr)
	def _extract_const_value(self, symtype):
		"""Extract concrete constant value from symbolic type."""
		try:
			# Check if this is a symbolic integer with name 'const'
			if hasattr(symtype, 'name') and symtype.name == 'const':
				# Try to get the concrete value
				if hasattr(symtype, 'getConcrValue'):
					return symtype.getConcrValue()
				elif hasattr(symtype, 'val'):
					return symtype.val
			
			# Check if it's an expression containing 'const'
			if hasattr(symtype, 'expr') and symtype.expr is not None:
				# Try to parse the expression to find constant value
				# For simple expressions like ["<", SymbolicInteger("a", 0), SymbolicInteger("const", 0)]
				if isinstance(symtype.expr, list) and len(symtype.expr) >= 3:
					for item in symtype.expr[1:]:
						if hasattr(item, 'name') and item.name == 'const':
							if hasattr(item, 'getConcrValue'):
								return item.getConcrValue()
							elif hasattr(item, 'val'):
								return item.val
		except Exception as e:
			# If extraction fails, return None
			pass
		return None

	def getVars(self):
		return self.vars

	def get_path_predicates(self):
		"""Return a list representation of this predicate for path reconstruction."""
		pred_dict = {
			'expr': self.expr,
			'result': self.result,
			'source_file': self.source_file,
			'source_line': self.source_line,
			'branch_id': self.branch_id,
			'vars': self.vars,
			'expr_tree': self.expr_tree  # Add tree structure
		}
		# Add constants if available
		if self.constants:
			pred_dict['constants'] = self.constants
		return [pred_dict]

	def to_dict(self):
		"""Convert predicate to dictionary representation."""
		pred_dict = {
			'expr': self.expr,
			'result': self.result,
			'source_file': self.source_file,
			'source_line': self.source_line,
			'branch_id': self.branch_id,
			'vars': self.vars,
			'expr_tree': self.expr_tree  # Add tree structure
		}
		# Add constants if available
		if self.constants:
			pred_dict['constants'] = self.constants
		return pred_dict

	def __eq__(self, other):
		if isinstance(other, Predicate):
			res = self.result == other.result and self.symtype.symbolicEq(other.symtype)
			return res
		else:
			return False

	def __hash__(self):
		return hash(self.symtype)

	def __str__(self):
		base_str = self.expr + " (%s)" % (self.result)
		if self.source_file and self.source_line:
			base_str += f" @ {self.source_file}:{self.source_line}"
		if self.branch_id:
			base_str += f" [branch:{self.branch_id}]"
		return base_str

	def __repr__(self):
		return self.__str__()

	def negate(self):
		"""Negates the current predicate"""
		assert(self.result is not None)
		self.result = not self.result
	
	def _parse_to_tree(self, expr_str):
		"""
		Parse string expression to tree structure.
		
		Example: "(< a#0, const#0)" -> ["<", "a", 0]
		
		Args:
			expr_str: String expression
		
		Returns:
			Tree structure representation
		"""
		import re
		
		# Remove outer parentheses if present
		expr = expr_str.strip()
		if expr.startswith('(') and expr.endswith(')'):
			expr = expr[1:-1]
		
		# Split by comma for binary operations
		parts = expr.split(', ')
		if len(parts) == 2:
			# Binary operation pattern: operator left_operand, right_operand
			# e.g.: "< a#0, const#0"
			
			# Extract operator (first word)
			op_match = re.match(r'([<>=!]=?|and|or|not)\s+', parts[0])
			if op_match:
				op = op_match.group(1)
				left = parts[0][len(op):].strip()
				right = parts[1].strip()
				
				# Clean variable names (remove # suffixes)
				left = re.sub(r'#\d+', '', left)
				right = re.sub(r'#\d+', '', right)
				
				# Handle constants
				if left.startswith('const'):
					left = self.constants.get('const', 0)
				elif left.replace('.', '', 1).isdigit():
					left = int(left) if '.' not in left else float(left)
				
				if right.startswith('const'):
					right = self.constants.get('const', 0)
				elif right.replace('.', '', 1).isdigit():
					right = int(right) if '.' not in right else float(right)
				
				return [op, left, right]
		
		# Fallback: return original string wrapped in list
		return ["raw", expr_str]
	
	def get_formula_deep(self):
		"""
		Get formula in deep mode (full expression).
		
		Returns:
			SMT formula string
		"""
		return self._get_formula(self.expr_tree, True)
	
	def get_formula_shallow(self):
		"""
		Get formula in shallow mode (concrete values).
		
		Returns:
			SMT formula string
		"""
		return self._get_formula(self.expr_tree, False)
	
	@staticmethod
	def _get_formula(expr_tree, deep):
		"""
		Convert expression tree to SMT formula.
		
		Args:
			expr_tree: Expression tree
			deep: Whether to get deep representation
		
		Returns:
			SMT formula string
		"""
		if isinstance(expr_tree, list):
			if expr_tree[0] == "raw":
				# Raw string fallback
				return expr_tree[1]
			
			# Recursively process tree
			op = expr_tree[0]
			operands = []
			for operand in expr_tree[1:]:
				if isinstance(operand, list):
					operands.append(Predicate._get_formula(operand, deep))
				elif deep or isinstance(operand, str):
					operands.append(str(operand))
				else:
					# In shallow mode, use concrete values for non-strings
					operands.append(str(operand))
			
			return f"({op} {' '.join(operands)})"
		
		# Simple value
		return str(expr_tree)

