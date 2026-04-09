# Copyright: see copyright.txt

import logging

log = logging.getLogger("se.constraint")

class Constraint:
	cnt = 0
	"""A constraint is a list of predicates leading to some specific
	   position in the code."""
	def __init__(self, parent, last_predicate):
		self.inputs = None
		self.predicate = last_predicate
		self.processed = False
		self.parent = parent
		self.children = []
		self.id = self.__class__.cnt
		self.__class__.cnt += 1

	def __eq__(self, other):
		"""Two Constraints are equal iff they have the same chain of predicates"""
		if isinstance(other, Constraint):
			if not self.predicate == other.predicate:
				return False
			return self.parent is other.parent
		else:
			return False

	def getAssertsAndQuery(self):
		self.processed = True

		# collect the assertions
		asserts = []
		tmp = self.parent
		while tmp.predicate is not None:
			asserts.append(tmp.predicate)
			tmp = tmp.parent

		return asserts, self.predicate	       

	def getLength(self):
		if self.parent == None:
			return 0
		return 1 + self.parent.getLength()

	def __str__(self):
		return str(self.predicate) + "  (processed: %s, path_len: %d)" % (self.processed,self.getLength())

	def __repr__(self):
		s = repr(self.predicate) + " (processed: %s)" % (self.processed)
		if self.parent is not None:
			s += "\n  path: %s" % repr(self.parent)
		return s

	def findChild(self, predicate):
		for c in self.children:
			if predicate == c.predicate:
				return c
		return None

	def addChild(self, predicate):
		assert(self.findChild(predicate) is None)
		c = Constraint(self, predicate)
		self.children.append(c)
		return c

	def get_path_predicates(self):
		"""Return all predicates in this constraint path."""
		predicates = []
		current = self
		while current is not None and current.predicate is not None:
			if hasattr(current.predicate, 'get_path_predicates'):
				predicates.extend(current.predicate.get_path_predicates())
			else:
				# Fallback for old predicate format
				predicates.append({
					'expr': str(current.predicate.symtype) if hasattr(current.predicate, 'symtype') else str(current.predicate),
					'result': current.predicate.result,
					'source_file': None,
					'source_line': None,
					'branch_id': None,
					'vars': current.predicate.getVars() if hasattr(current.predicate, 'getVars') else []
				})
			current = current.parent
		# Reverse to get from root to leaf
		return list(reversed(predicates))

	def to_dict(self):
		"""Convert constraint to dictionary representation."""
		return {
			'id': self.id,
			'predicate': self.predicate.to_dict() if hasattr(self.predicate, 'to_dict') else {
				'expr': str(self.predicate.symtype) if hasattr(self.predicate, 'symtype') else str(self.predicate),
				'result': self.predicate.result
			},
			'processed': self.processed,
			'path_length': self.getLength(),
			'path_predicates': self.get_path_predicates(),
			'children_ids': [c.id for c in self.children]
		}

