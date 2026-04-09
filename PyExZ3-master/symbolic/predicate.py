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
		self.vars = st.getVars() if hasattr(st, 'getVars') else []

	def getVars(self):
		return self.vars

	def get_path_predicates(self):
		"""Return a list representation of this predicate for path reconstruction."""
		return [{
			'expr': self.expr,
			'result': self.result,
			'source_file': self.source_file,
			'source_line': self.source_line,
			'branch_id': self.branch_id,
			'vars': self.vars
		}]

	def to_dict(self):
		"""Convert predicate to dictionary representation."""
		return {
			'expr': self.expr,
			'result': self.result,
			'source_file': self.source_file,
			'source_line': self.source_line,
			'branch_id': self.branch_id,
			'vars': self.vars
		}

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

