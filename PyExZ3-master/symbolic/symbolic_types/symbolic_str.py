from . symbolic_type import SymbolicObject
from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from string import whitespace

class SymbolicStr(SymbolicObject, str):

    def __new__(cls, name, v, expr=None):
        return str.__new__(cls, v)

    def __init__(self, name, v, expr=None):
        SymbolicObject.__init__(self, name, expr)
        self.val = v

    def getConcrValue(self):
        return self.val

    def wrap(conc, sym):
        return SymbolicStr("se", conc, sym)

    def __hash__(self):
        return hash(self.val)

    def _op_worker(self, args, fun, op):
        return self._do_sexpr(args, fun, op, SymbolicStr.wrap)

    def __bool__(self):
        return SymbolicObject.__bool__(self.__len__() != 0)

    def __len__(self):
        return self._do_sexpr([self], lambda x: len(x),
                                "str.len", SymbolicInteger.wrap)

    def __contains__(self, item):
        return self._do_sexpr([self, item], lambda x, y: str.__contains__(x, y),
                                "in", SymbolicInteger.wrap)

    def __getitem__(self, key):
        """Negative indexes, out of bound slices, and slice skips are not currently supported."""
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else self.__len__()
            return self._do_sexpr([self, start, stop],
                                  lambda x, y, z: str.__getitem__(x, slice(y, z)), "slice", SymbolicStr.wrap)
        return self._do_sexpr([self, key], lambda x, y: str.__getitem__(x, y),
                              "getitem", SymbolicStr.wrap)

    def find(self, findstr, beg=0):
        return self._do_sexpr([self, findstr, beg],
                              lambda x, y, z: str.find(x, y, z),
                              "str.find", SymbolicInteger.wrap)

    def startswith(self, prefix):
        return self._do_sexpr([self, prefix],
                              lambda x, y: str.startswith(x, y),
                              "str.startswith", SymbolicInteger.wrap)

    def split(self, sep=None, maxsplit=None):
        if sep is None:
            sep = " "
        if len(self) == 0:
            return []
        elif maxsplit == 0 or sep not in self:
            return [self]
        else:
            sep_idx = self.find(sep)
            maxsplit = None if maxsplit is None else maxsplit - 1
            return [self[0:sep_idx]] + \
                   self[sep_idx + 1:].split(sep, maxsplit)

    def count(self, sub):
        """String count is not a native function of the SMT solver. Instead, we implement count as a recursive series of
        find operations. Note that not all of the functionality of count is supported at this time, such as the start
        index."""
        if sub not in self:
            ret = 0
        elif sub == "":
            ret = self.__len__() + 1
        else:
            find_idx = self.find(sub)
            reststr = self[find_idx + sub.__len__():]
            ret = reststr.count(sub) + 1
        assert int(ret) == str.count(str(self), str(sub))
        return ret

    def _replace(self, old, new):
        return self._do_sexpr([self, old, new], lambda x, y, z: str.replace(x, y, z),
                              "str.replace", SymbolicStr.wrap)

    def replace(self, old, new, maxreplace=-1):
        """CVC only replaces the first occurrence of old with new
        (maxreplace=1). For this reason, SymbolicStr's replace is implemented
        as a recurrence of single replaces."""
        if maxreplace == 0 or old not in self:
            ret = self
        else:
            pivot_point = self.find(old) + old.__len__()
            first_half = self[:pivot_point]
            first_half = first_half._replace(old, new)
            second_half = self[pivot_point:]
            ret = first_half + second_half.replace(old, new, maxreplace-1)
        assert str(ret) == str.replace(str(self), str(old), str(new), int(maxreplace))
        return ret

    def strip(self, chars=None):
        if chars is None:
            chars = whitespace
        if self.__len__() == 0:
            return self
        for char in chars:
            if self[0] == char:
                return self[1:].strip(chars)
        for char in chars:
            if self[self.__len__() - 1] == char:
                return self[:self.__len__() - 1].strip(chars)
        return self
    
    # New string methods for PyCT compatibility
    
    def endswith(self, suffix):
        return self._do_sexpr([self, suffix],
                              lambda x, y: str.endswith(x, y),
                              "str.endswith", SymbolicInteger.wrap)
    
    def index(self, sub, beg=0, end=None):
        # Similar to find but raises ValueError if not found
        # For symbolic execution, we treat it similar to find
        if end is None:
            end = self.__len__()
        return self._do_sexpr([self, sub, beg, end],
                              lambda x, y, z, w: str.index(x, y, z, w) if y in x[z:w] else -1,
                              "str.index", SymbolicInteger.wrap)
    
    def isalpha(self):
        return self._do_sexpr([self],
                              lambda x: str.isalpha(x),
                              "str.isalpha", SymbolicInteger.wrap)
    
    def isdigit(self):
        return self._do_sexpr([self],
                              lambda x: str.isdigit(x),
                              "str.isdigit", SymbolicInteger.wrap)
    
    def islower(self):
        return self._do_sexpr([self],
                              lambda x: str.islower(x),
                              "str.islower", SymbolicInteger.wrap)
    
    def isupper(self):
        return self._do_sexpr([self],
                              lambda x: str.isupper(x),
                              "str.isupper", SymbolicInteger.wrap)
    
    def lower(self):
        return self._do_sexpr([self],
                              lambda x: str.lower(x),
                              "str.lower", SymbolicStr.wrap)
    
    def upper(self):
        return self._do_sexpr([self],
                              lambda x: str.upper(x),
                              "str.upper", SymbolicStr.wrap)
    
    def capitalize(self):
        """Return a capitalized version of the string."""
        return self._do_sexpr([self],
                              lambda x: str.capitalize(x),
                              "str.capitalize", SymbolicStr.wrap)
    
    def swapcase(self):
        """Return a copy of the string with uppercase characters converted to lowercase and vice versa."""
        return self._do_sexpr([self],
                              lambda x: str.swapcase(x),
                              "str.swapcase", SymbolicStr.wrap)
    
    def title(self):
        """Return a titlecased version of the string where words start with an uppercase character and the remaining characters are lowercase."""
        return self._do_sexpr([self],
                              lambda x: str.title(x),
                              "str.title", SymbolicStr.wrap)
    
    def center(self, width, fillchar=' '):
        """Return centered in a string of length width."""
        return self._do_sexpr([self, width, fillchar],
                              lambda x, w, f: str.center(x, w, f),
                              "str.center", SymbolicStr.wrap)
    
    def zfill(self, width):
        """Pad a numeric string with zeros on the left, to fill a field of the given width."""
        return self._do_sexpr([self, width],
                              lambda x, w: str.zfill(x, w),
                              "str.zfill", SymbolicStr.wrap)
    
    def partition(self, sep):
        """Split the string at the first occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator."""
        # partition returns a tuple of 3 strings
        # We need to handle this specially since _do_sexpr expects a single return value
        # For now, we'll return a concrete tuple
        before, sep_str, after = str.partition(self.val, sep)
        # Create SymbolicStr objects for each part
        # Note: This loses symbolic relationships but provides basic functionality
        return (SymbolicStr("part_before", before),
                SymbolicStr("sep", sep_str),
                SymbolicStr("part_after", after))
    
    def rpartition(self, sep):
        """Split the string at the last occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator."""
        # Similar to partition, returns a tuple of 3 strings
        # For now, we'll return a concrete tuple
        before, sep_str, after = str.rpartition(self.val, sep)
        return (SymbolicStr("rpart_before", before),
                SymbolicStr("rsep", sep_str),
                SymbolicStr("rpart_after", after))
    
    def rfind(self, sub, start=0, end=None):
        """Return the highest index in the string where substring sub is found."""
        if end is None:
            end = self.__len__()
        return self._do_sexpr([self, sub, start, end],
                              lambda x, s, st, e: str.rfind(x, s, st, e),
                              "str.rfind", SymbolicInteger.wrap)
    
    def rindex(self, sub, start=0, end=None):
        """Like rfind() but raise ValueError when the substring is not found."""
        if end is None:
            end = self.__len__()
        
        # Helper function to get concrete value if possible
        def get_concrete_value(obj):
            if hasattr(obj, 'getConcrValue'):
                return obj.getConcrValue()
            return obj
        
        # Check if we can get concrete values for all parameters
        try:
            # Get concrete values
            s_val = self.getConcrValue()
            sub_val = get_concrete_value(sub)
            start_val = get_concrete_value(start)
            end_val = get_concrete_value(end)
            
            # All parameters have concrete values, use Python's str.rindex
            # This will raise ValueError if substring not found
            result = str.rindex(s_val, sub_val, start_val, end_val)
            
            # Return as SymbolicInteger
            from .symbolic_int import SymbolicInteger
            return SymbolicInteger("rindex_result", result, ["str.rindex", self.expr if not self.isVariable() else self.name])
            
        except (AttributeError, TypeError):
            # Some parameter doesn't have concrete value, use symbolic execution
            # For symbolic strings, we can't know if substring exists at analysis time
            # So we return a symbolic result that might be -1 if substring not found
            return self._do_sexpr([self, sub, start, end],
                                  lambda x, s, st, e: str.rindex(x, s, st, e) if str.rfind(x, s, st, e) != -1 else -1,
                                  "str.rindex", SymbolicInteger.wrap)
    
    def isalnum(self):
        return self._do_sexpr([self],
                              lambda x: str.isalnum(x),
                              "str.isalnum", SymbolicInteger.wrap)
    
    def isnumeric(self):
        return self._do_sexpr([self],
                              lambda x: str.isnumeric(x),
                              "str.isnumeric", SymbolicInteger.wrap)
    
    # Additional check methods
    def isascii(self):
        """Return True if all characters in the string are ASCII."""
        return self._do_sexpr([self],
                              lambda x: str.isascii(x),
                              "str.isascii", SymbolicInteger.wrap)
    
    def isdecimal(self):
        """Return True if all characters in the string are decimal."""
        return self._do_sexpr([self],
                              lambda x: str.isdecimal(x),
                              "str.isdecimal", SymbolicInteger.wrap)
    
    def isidentifier(self):
        """Return True if the string is a valid identifier."""
        return self._do_sexpr([self],
                              lambda x: str.isidentifier(x),
                              "str.isidentifier", SymbolicInteger.wrap)
    
    def isprintable(self):
        """Return True if all characters in the string are printable."""
        return self._do_sexpr([self],
                              lambda x: str.isprintable(x),
                              "str.isprintable", SymbolicInteger.wrap)
    
    def isspace(self):
        """Return True if all characters in the string are whitespace."""
        return self._do_sexpr([self],
                              lambda x: str.isspace(x),
                              "str.isspace", SymbolicInteger.wrap)
    
    def istitle(self):
        """Return True if the string is titlecased."""
        return self._do_sexpr([self],
                              lambda x: str.istitle(x),
                              "str.istitle", SymbolicInteger.wrap)
    
    def casefold(self):
        """Return a version of the string suitable for caseless comparisons."""
        return self._do_sexpr([self],
                              lambda x: str.casefold(x),
                              "str.casefold", SymbolicStr.wrap)
    
    def expandtabs(self, tabsize=8):
        """Return a copy of the string where all tab characters are replaced by spaces."""
        return self._do_sexpr([self, tabsize],
                              lambda x, t: str.expandtabs(x, t),
                              "str.expandtabs", SymbolicStr.wrap)
    
    def ljust(self, width, fillchar=' '):
        """Return the string left justified in a string of length width."""
        return self._do_sexpr([self, width, fillchar],
                              lambda x, w, f: str.ljust(x, w, f),
                              "str.ljust", SymbolicStr.wrap)
    
    def rjust(self, width, fillchar=' '):
        """Return the string right justified in a string of length width."""
        return self._do_sexpr([self, width, fillchar],
                              lambda x, w, f: str.rjust(x, w, f),
                              "str.rjust", SymbolicStr.wrap)
    
    def rsplit(self, sep=None, maxsplit=-1):
        """Return a list of the words in the string, using sep as the delimiter string."""
        # For simplicity, we'll implement a basic version that returns a concrete list
        # In a full implementation, we would need to handle symbolic relationships
        if sep is None:
            sep = " "
        # For now, use concrete value
        concrete_result = self.val.rsplit(sep, maxsplit)
        # Convert to SymbolicStr objects
        from .symbolic_str import SymbolicStr
        return [SymbolicStr(f"rsplit_part_{i}", part) for i, part in enumerate(concrete_result)]
    
    def translate(self, table):
        """Return a copy of the string in which each character has been mapped through the given translation table."""
        # For now, use concrete value
        return self._do_sexpr([self, table],
                              lambda x, t: str.translate(x, t),
                              "str.translate", SymbolicStr.wrap)
    
    def lstrip(self, chars=None):
        if chars is None:
            chars = whitespace
        if self.__len__() == 0:
            return self
        for char in chars:
            if self[0] == char:
                return self[1:].lstrip(chars)
        return self
    
    def rstrip(self, chars=None):
        if chars is None:
            chars = whitespace
        if self.__len__() == 0:
            return self
        for char in chars:
            if self[self.__len__() - 1] == char:
                return self[:self.__len__() - 1].rstrip(chars)
        return self
    
    def splitlines(self, keepends=False):
        # Simple implementation for splitlines
        # For symbolic execution, we return a list with self if no newlines
        if "\n" not in self and "\r" not in self:
            return [self]
        # Otherwise, we need to handle symbolically - return a list with the string
        # This is a simplified implementation
        return [self]
    
    # Advanced string methods
    def format(self, *args, **kwargs):
        """String formatting operation - str.format()
        For symbolic execution, this is complex. We'll provide a basic implementation
        that returns the string itself for now."""
        # This is a simplified implementation
        # In a full implementation, we would need to handle format specifiers
        # For now, we handle the simple case with no arguments
        if len(args) == 0 and len(kwargs) == 0:
            return self._do_sexpr([self],
                                  lambda x: x,
                                  "str.format", SymbolicStr.wrap)
        # With arguments, we need to handle them properly
        # Since _do_sexpr expects a lambda with specific parameter names,
        # we'll create a simpler implementation for now
        try:
            # Try to format concretely for now
            concrete_result = self.val.format(*args, **kwargs)
            return SymbolicStr("format_result", concrete_result, 
                              ["str.format", self.expr if not self.isVariable() else self.name] + list(args))
        except:
            # Fallback: return self
            return self
    
    def join(self, iterable):
        """String join operation - str.join()
        For symbolic execution, joining symbolic strings is complex.
        We'll provide a basic implementation."""
        # Simple implementation: join with the separator
        return self._do_sexpr([self, iterable],
                              lambda sep, it: sep.join(it),
                              "str.join", SymbolicStr.wrap)
    
    def encode(self, encoding='utf-8', errors='strict'):
        """String encoding operation - str.encode()
        Returns bytes. For symbolic execution, we return symbolic bytes.
        This is a simplified implementation."""
        # For now, encode the concrete value
        # In a full implementation, we would create a SymbolicBytes type
        encoded_bytes = self.val.encode(encoding, errors)
        # Return as bytes (not yet symbolic)
        return encoded_bytes
    
    def decode(self, encoding='utf-8', errors='strict'):
        """Bytes decoding operation - bytes.decode()
        Note: This is actually a bytes method, not a string method.
        We include it here for completeness, but it should be called on bytes."""
        # This method doesn't make sense for strings, but we include a placeholder
        raise TypeError("decode() argument must be bytes, not str")
    
    # Comparison methods for partial support
    def __lt__(self, other):
        return self._do_sexpr([self, other],
                              lambda x, y: str.__lt__(x, y),
                              "str.lt", SymbolicInteger.wrap)
    
    def __le__(self, other):
        return self._do_sexpr([self, other],
                              lambda x, y: str.__le__(x, y),
                              "str.le", SymbolicInteger.wrap)
    
    def __gt__(self, other):
        return self._do_sexpr([self, other],
                              lambda x, y: str.__gt__(x, y),
                              "str.gt", SymbolicInteger.wrap)
    
    def __ge__(self, other):
        return self._do_sexpr([self, other],
                              lambda x, y: str.__ge__(x, y),
                              "str.ge", SymbolicInteger.wrap)
    
    # Mod (format) operation - partial support
    def __mod__(self, other):
        # String formatting - for symbolic execution, we return the string itself
        # This is a simplified implementation
        return self._do_sexpr([self, other],
                              lambda x, y: str.__mod__(x, y) if isinstance(y, tuple) else x % y,
                              "str.mod", SymbolicStr.wrap)
    
    def __rmod__(self, other):
        # Right modulo for string formatting
        return self._do_sexpr([other, self],
                              lambda x, y: str.__rmod__(x, y) if isinstance(x, tuple) else x % y,
                              "str.rmod", SymbolicStr.wrap)

# Currently only a subset of string operations are supported.
ops = [("add", "+"), ("mul", "*")]

def make_method(method,op,a):
    code  = "def %s(self,other):\n" % method
    code += "   return self._op_worker(%s,lambda x,y : x %s y, \"%s\")" % (a,op,op)
    locals_dict = {}
    exec(code, globals(), locals_dict)
    setattr(SymbolicStr, method, locals_dict[method])

for (name,op) in ops:
    method  = "__%s__" % name
    make_method(method,op,"[self,other]")
    rmethod  = "__r%s__" % name
    make_method(rmethod,op,"[other,self]")

