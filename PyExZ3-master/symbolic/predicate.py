# Copyright - see copyright.txt

class Predicate:
	"""Predicate is one specific ``if'' encountered during the program execution.
	   """
	def __init__(self, st, result, source_file=None, source_line=None, branch_id=None, col=None):
		self.symtype = st
		self.result = result
		self.source_file = source_file
		self.source_line = source_line
		self.branch_id = branch_id
		self.col = col

	def getVars(self):
		return self.symtype.getVars()

	def __eq__(self, other):
		if isinstance(other, Predicate):
			res = self.result == other.result and self.symtype.symbolicEq(other.symtype)
			return res
		else:
			return False

	def __hash__(self):
		return hash(self.symtype)

	def _get_symbolic_expr(self, symtype):
		"""Get stable symbolic expression representation without concrete values"""
		if symtype.isVariable():
			return symtype.name
		elif hasattr(symtype, 'expr') and symtype.expr:
			return self._format_expr(symtype.expr)
		else:
			return str(symtype)

	def _format_expr(self, expr):
		"""Format expression without concrete values"""
		if isinstance(expr, list):
			op = expr[0]
			args = expr[1:]
			formatted_args = [self._format_expr(arg) for arg in args]
			return f"({op} {' '.join(formatted_args)})"
		elif hasattr(expr, 'name'):
			return expr.name
		else:
			return str(expr)

	def __str__(self):
		loc = ""  
		if self.source_file and self.source_line:
			if self.col:
				loc = f" at {self.source_file}:{self.source_line}:{self.col}"
			else:
				loc = f" at {self.source_file}:{self.source_line}"
		return self.symtype.toString() + " (%s)%s" % (self.result, loc)

	def __repr__(self):
		return self.__str__()

	def negate(self):
		"""Negates the current predicate"""
		assert(self.result is not None)
		self.result = not self.result

	def to_dict(self):
		"""Convert predicate to dictionary for JSON export"""
		return {
			"expr": self._get_symbolic_expr(self.symtype),
			"result": self.result,
			"source_file": self.source_file,
			"source_line": self.source_line,
			"source_col": self.col,
			"branch_id": self.branch_id,
			"vars": list(self.getVars())
		}

	def get_symbolic_expr(self):
		"""Get stable symbolic expression representation"""
		return self._get_symbolic_expr(self.symtype)

