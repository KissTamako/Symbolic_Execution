# Copyright - see copyright.txt

class Predicate:
	"""Predicate is one specific ``if'' encountered during the program execution.
	   """
	def __init__(self, st, result, source_file=None, source_line=None, branch_id=None):
		self.symtype = st
		self.result = result
		self.source_file = source_file
		self.source_line = source_line
		self.branch_id = branch_id

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

	def __str__(self):
		loc = ""  
		if self.source_file and self.source_line:
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
			"expr": self.symtype.toString(),
			"result": self.result,
			"source_file": self.source_file,
			"source_line": self.source_line,
			"branch_id": self.branch_id,
			"vars": list(self.getVars())
		}

