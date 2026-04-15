from . symbolic_type import SymbolicObject
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

    def _op_worker(self, args, fun, op, wrap=None):
        if wrap is None:
            wrap = SymbolicStr.wrap
        return self._do_sexpr(args, fun, op, wrap)

    # 布尔转换 - 使用基类实现
    def __bool__(self):
        return super(SymbolicStr, self).__bool__()

    def __len__(self):
        from . symbolic_int import SymbolicInteger
        return self._do_sexpr([self], lambda x: len(x),
                                "str.len", SymbolicInteger.wrap)

    def __contains__(self, item):
        from . symbolic_bool import SymbolicBool
        return self._do_sexpr([self, item], lambda x, y: str.__contains__(x, y),
                                "in", SymbolicBool.wrap)

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
        from . symbolic_int import SymbolicInteger
        return self._do_sexpr([self, findstr, beg],
                              lambda x, y, z: str.find(x, y, z),
                              "str.find", SymbolicInteger.wrap)

    def startswith(self, prefix):
        from . symbolic_bool import SymbolicBool
        return self._do_sexpr([self, prefix],
                              lambda x, y: str.startswith(x, y),
                              "str.startswith", SymbolicBool.wrap)

    def endswith(self, suffix):
        from . symbolic_bool import SymbolicBool
        return self._do_sexpr([self, suffix],
                              lambda x, y: str.endswith(x, y),
                              "str.endswith", SymbolicBool.wrap)

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

    def upper(self):
        """Return a copy of the string converted to uppercase."""
        value = self.val.upper()
        # 简单实现，实际应该使用str.replaceall
        return SymbolicStr("se", value)

    def lower(self):
        """Return a copy of the string converted to lowercase."""
        value = self.val.lower()
        # 简单实现，实际应该使用str.replaceall
        return SymbolicStr("se", value)

    def capitalize(self):
        """Return a capitalized version of the string."""
        value = self.val.capitalize()
        return SymbolicStr("se", value)

    def isalnum(self):
        """Return True if the string is an alpha-numeric string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.isalnum()
        return SymbolicBool("se", value)

    def isalpha(self):
        """Return True if the string is an alphabetic string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.isalpha()
        return SymbolicBool("se", value)

    def isdigit(self):
        """Return True if the string is a digit string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.isdigit()
        return SymbolicBool("se", value)

    def islower(self):
        """Return True if the string is a lowercase string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.islower()
        return SymbolicBool("se", value)

    def isupper(self):
        """Return True if the string is an uppercase string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.isupper()
        return SymbolicBool("se", value)

    def isspace(self):
        """Return True if the string is a whitespace string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.isspace()
        return SymbolicBool("se", value)

    def istitle(self):
        """Return True if the string is a title-cased string, False otherwise."""
        from . symbolic_bool import SymbolicBool
        value = self.val.istitle()
        return SymbolicBool("se", value)

    # 辅助方法
    def __bool2__(self):
        """Convert to symbolic bool"""
        from . symbolic_bool import SymbolicBool
        value = bool(self.val)
        expr = ["not", ["=", self, ""]]
        return SymbolicBool("se", value, expr)

    def __int2__(self):
        """Convert to symbolic int"""
        from . symbolic_int import SymbolicInteger
        value = int(self.val)
        # 处理负数的情况
        if self.val.startswith('-'):
            expr = ["-", ["str.to.int", ["str.substr", self, 1, ["str.len", self]]]]
        else:
            expr = ["str.to.int", self]
        return SymbolicInteger("se", value, expr)

    def __str2__(self):
        """Convert to symbolic string"""
        return self

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

