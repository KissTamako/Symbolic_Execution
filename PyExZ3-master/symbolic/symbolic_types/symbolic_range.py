# Copyright: see copyright.txt

from . symbolic_type import SymbolicObject
from symbolic.symbolic_types.symbolic_int import SymbolicInteger

class SymbolicRange(SymbolicObject):
    """
    Symbolic representation of Python's range type.
    A concolic range maintains both concrete and symbolic representations.
    Concrete value: the actual sequence of integers
    Symbolic expression: quadruple (start, stop, step, current)
    """
    
    def __new__(cls, name, v, expr=None):
        # Since range is not a base type like int/str, we don't need __new__
        return object.__new__(cls)
    
    def __init__(self, name, v, expr=None):
        """
        Initialize a symbolic range.
        v should be a range object or tuple (start, stop, step)
        expr should be a symbolic expression or None for variables
        """
        SymbolicObject.__init__(self, name, expr)
        
        if isinstance(v, range):
            self.range_obj = v
            self.start = v.start
            self.stop = v.stop
            self.step = v.step
        elif isinstance(v, tuple) and len(v) == 3:
            self.start, self.stop, self.step = v
            self.range_obj = range(self.start, self.stop, self.step)
        else:
            raise ValueError("SymbolicRange requires a range object or (start, stop, step) tuple")
        
        self.val = self.range_obj
        self.current_index = 0  # For iteration
    
    def getConcrValue(self):
        return self.range_obj
    
    def wrap(conc, sym):
        """Wrap concrete range and symbolic expression into SymbolicRange"""
        if isinstance(conc, range):
            return SymbolicRange("se", conc, sym)
        else:
            # Assume it's a tuple (start, stop, step)
            return SymbolicRange("se", conc, sym)
    
    def __hash__(self):
        return hash(self.range_obj)
    
    def _op_worker(self, args, fun, op):
        return self._do_sexpr(args, fun, op, SymbolicRange.wrap)
    
    # Required methods for PyCT compatibility
    
    def __contains__(self, item):
        """Check if item is in the range"""
        # For symbolic execution, we need to create a constraint
        # item >= start AND item < stop AND (item - start) % step == 0
        # This is complex, so we'll implement a simplified version
        return self._do_sexpr([self, item],
                             lambda x, y: y in x,
                             "range.contains", SymbolicInteger.wrap)
    
    def __iter__(self):
        """Return an iterator over the range"""
        # For symbolic execution, we need to track iteration
        # We'll return a special iterator that can generate constraints
        self.current_index = 0
        return self
    
    def __next__(self):
        """Get next element in iteration"""
        if self.current_index >= len(self.range_obj):
            raise StopIteration
        
        # Get current value
        current_val = self.range_obj[self.current_index]
        
        # For symbolic execution, we need to create a constraint
        # that relates current_val to start, step, and index
        # current_val = start + step * current_index
        # AND current_index < len(range)
        
        self.current_index += 1
        return SymbolicInteger("range_elem", current_val, 
                              ["range_elem", self.start, self.step, self.current_index - 1])
    
    def __len__(self):
        """Get length of the range"""
        return self._do_sexpr([self],
                             lambda x: len(x),
                             "range.len", SymbolicInteger.wrap)
    
    def count(self, value):
        """Count occurrences of value in range (0 or 1 for ranges)"""
        return self._do_sexpr([self, value],
                             lambda x, y: x.count(y),
                             "range.count", SymbolicInteger.wrap)
    
    def index(self, value):
        """Get index of value in range"""
        return self._do_sexpr([self, value],
                             lambda x, y: x.index(y) if y in x else -1,
                             "range.index", SymbolicInteger.wrap)
    
    def __getitem__(self, key):
        """Get item at index or slice"""
        if isinstance(key, slice):
            # Return a new range for the slice
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self)
            step = key.step if key.step is not None else 1
            
            new_start = self.range_obj[start]
            new_stop = self.range_obj[stop] if stop < len(self) else self.stop
            new_step = self.step * step
            
            new_range = range(new_start, new_stop, new_step)
            return SymbolicRange("slice", new_range,
                                ["range_slice", self.start, self.stop, self.step, start, stop, step])
        else:
            # Single index
            return self._do_sexpr([self, key],
                                 lambda x, y: x[y],
                                 "range.getitem", SymbolicInteger.wrap)
    
    # Representation methods
    def __repr__(self):
        return f"SymbolicRange({self.range_obj})"
    
    def __str__(self):
        return str(self.range_obj)
    
    # Properties for compatibility
    @property
    def start(self):
        return self._start
    
    @start.setter
    def start(self, value):
        self._start = value
    
    @property
    def stop(self):
        return self._stop
    
    @stop.setter 
    def stop(self, value):
        self._stop = value
    
    @property
    def step(self):
        return self._step
    
    @step.setter
    def step(self, value):
        self._step = value
    
    # Methods that are not supported (return concrete values)
    def __bool__(self):
        # Range is truthy if non-empty
        # For symbolic execution, we need to return a symbolic boolean
        # But __bool__ must return actual bool, so we return concrete
        return bool(self.range_obj)
    
    def __eq__(self, other):
        # Compare ranges symbolically
        # For symbolic execution, we create a symbolic expression
        # comparing start, stop, and step values
        if isinstance(other, SymbolicRange):
            # Compare all three components
            start_eq = self.start == other.start
            stop_eq = self.stop == other.stop  
            step_eq = self.step == other.step
            # Range equality requires all three components to be equal
            return self._do_sexpr([self, other],
                                 lambda x, y: x.range_obj == y.range_obj,
                                 "range.eq", SymbolicInteger.wrap)
        elif isinstance(other, range):
            # Compare with concrete range
            start_eq = self.start == other.start
            stop_eq = self.stop == other.stop
            step_eq = self.step == other.step
            return self._do_sexpr([self, other],
                                 lambda x, y: x.range_obj == y,
                                 "range.eq", SymbolicInteger.wrap)
        else:
            # Not comparable
            return self._do_sexpr([self, other],
                                 lambda x, y: False,
                                 "range.eq", SymbolicInteger.wrap)
    
    def __ne__(self, other):
        # Range inequality
        return self._do_sexpr([self, other],
                             lambda x, y: x.range_obj != y.range_obj if isinstance(y, SymbolicRange) else x.range_obj != y,
                             "range.ne", SymbolicInteger.wrap)
    
    def __lt__(self, other):
        # Range less than - not typically meaningful, but we provide symbolic support
        # We compare based on start values
        if isinstance(other, SymbolicRange):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x < y,
                                 "range.lt", SymbolicInteger.wrap)
        elif isinstance(other, range):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x < y,
                                 "range.lt", SymbolicInteger.wrap)
        else:
            return self._do_sexpr([self, other],
                                 lambda x, y: False,
                                 "range.lt", SymbolicInteger.wrap)
    
    def __le__(self, other):
        # Range less than or equal
        if isinstance(other, SymbolicRange):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x <= y,
                                 "range.le", SymbolicInteger.wrap)
        elif isinstance(other, range):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x <= y,
                                 "range.le", SymbolicInteger.wrap)
        else:
            return self._do_sexpr([self, other],
                                 lambda x, y: False,
                                 "range.le", SymbolicInteger.wrap)
    
    def __gt__(self, other):
        # Range greater than
        if isinstance(other, SymbolicRange):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x > y,
                                 "range.gt", SymbolicInteger.wrap)
        elif isinstance(other, range):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x > y,
                                 "range.gt", SymbolicInteger.wrap)
        else:
            return self._do_sexpr([self, other],
                                 lambda x, y: False,
                                 "range.gt", SymbolicInteger.wrap)
    
    def __ge__(self, other):
        # Range greater than or equal
        if isinstance(other, SymbolicRange):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x >= y,
                                 "range.ge", SymbolicInteger.wrap)
        elif isinstance(other, range):
            return self._do_sexpr([self.start, other.start],
                                 lambda x, y: x >= y,
                                 "range.ge", SymbolicInteger.wrap)
        else:
            return self._do_sexpr([self, other],
                                 lambda x, y: False,
                                 "range.ge", SymbolicInteger.wrap)
    
    def __reversed__(self):
        # Return reversed concrete range
        # For symbolic execution, we should create a new SymbolicRange
        reversed_range = range(self.start + (len(self.range_obj) - 1) * self.step, 
                               self.start - self.step if self.start > self.stop else self.start + self.step, 
                               -self.step)
        return SymbolicRange("reversed", reversed_range,
                            ["range.reversed", self.start, self.stop, self.step])
