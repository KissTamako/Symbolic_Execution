from .symbolic_type import SymbolicType
from .symbolic_int import SymbolicInteger
from .symbolic_bool import SymbolicBool

# 避免循环导入，在需要时再导入

def unwrap(value):
    """Unwrap a symbolic value to get its concrete value"""
    if hasattr(value, 'getConcrValue'):
        return value.getConcrValue()
    return value

class SymbolicRange(SymbolicType):
    def __init__(self, *args):
        # 模拟range的构造
        unwrapped_args = [unwrap(arg) for arg in args]
        self.super = range(*unwrapped_args)
        
        # 处理参数
        if len(args) < 2:
            self.start = 0
            self.stop = args[0]
        else:
            self.start = args[0]
            self.stop = args[1]
        
        if len(args) < 3:
            self.step = 1
        else:
            self.step = args[2]
        
        # 确保所有属性都是符号整数
        if not isinstance(self.start, SymbolicInteger):
            if hasattr(self.start, '__int__'):
                self.start = SymbolicInteger(int(self.start))
            else:
                self.start = SymbolicInteger(self.super.start)
        
        if not isinstance(self.stop, SymbolicInteger):
            if hasattr(self.stop, '__int__'):
                self.stop = SymbolicInteger(int(self.stop))
            else:
                self.stop = SymbolicInteger(self.super.stop)
        
        if not isinstance(self.step, SymbolicInteger):
            if hasattr(self.step, '__int__'):
                self.step = SymbolicInteger(int(self.step))
            else:
                self.step = SymbolicInteger(self.super.step)
    
    def __bool__(self):
        """self != 0"""
        return SymbolicBool(bool(self.super))
    
    def __contains__(self, key):
        """Return key in self."""
        unwrapped_key = unwrap(key)
        value = unwrapped_key in self.super
        
        # 处理符号值
        if isinstance(key, SymbolicType):
            if self.start < self.stop:
                expr = (self.start <= key) & (key < self.stop) & (((key - self.start) % self.step) == 0)
                return SymbolicBool(value, expr)
            elif self.start > self.stop:
                expr = (self.start >= key) & (key > self.stop) & (((key - self.start) % self.step) == 0)
                return SymbolicBool(value, expr)
        
        return SymbolicBool(value)
    
    def __eq__(self, value):
        """Return self==value."""
        return SymbolicBool(self.super == unwrap(value))
    
    def __ge__(self, value):
        """Return self>=value."""
        return SymbolicBool(self.super >= unwrap(value))
    
    def __getitem__(self, key):
        """Return self[key]."""
        unwrapped_key = unwrap(key)
        value = self.super[unwrapped_key]
        
        # 处理切片
        if isinstance(key, slice) and key.start is None and key.stop is None and key.step == -1:
            if self.step > 0:
                k = (self.stop - self.start) // self.step - int((self.stop - self.start) % self.step == 0)
                start = self.start + k * self.step
                stop = self.start - self.step
                step = -self.step
                if start == value.start and stop == value.stop and step == value.step:
                    return self.__class__(start, stop, step)
        
        return SymbolicInteger(value)
    
    def __gt__(self, value):
        """Return self>value."""
        return SymbolicBool(self.super > unwrap(value))
    
    def __hash__(self):
        """Return hash(self)."""
        return hash(self.super)
    
    def __iter__(self):
        """Implement iter(self)."""
        current = self.start
        while True:
            if self.step > 0:
                if current < self.stop:
                    result = current
                    current += self.step
                    yield result
                else:
                    break
            else:  # self.step < 0
                if current > self.stop:
                    result = current
                    current += self.step
                    yield result
                else:
                    break
    
    def __le__(self, value):
        """Return self<=value."""
        return SymbolicBool(self.super <= unwrap(value))
    
    def __len__(self):
        """Return len(self)."""
        value = len(self.super)
        expr = ((self.stop - self.start) // self.step) + (((self.stop - self.start) % self.step) != 0)
        return SymbolicInteger(value, expr)
    
    def __lt__(self, value):
        """Return self<value."""
        return SymbolicBool(self.super < unwrap(value))
    
    def __ne__(self, value):
        """Return self!=value."""
        return SymbolicBool(self.super != unwrap(value))
    
    def __reversed__(self):
        """Return a reverse iterator."""
        return reversed(self.super)
    
    def count(self, key):
        """rangeobject.count(value) -> integer -- return number of occurrences of value"""
        unwrapped_key = unwrap(key)
        value = self.super.count(unwrapped_key)
        
        # 处理符号值
        if isinstance(key, SymbolicType):
            if self.start < self.stop:
                expr = ((self.start <= key) & (key < self.stop) & (((key - self.start) % self.step) == 0))
                return SymbolicInteger(value, expr)
            elif self.start > self.stop:
                expr = ((self.start >= key) & (key > self.stop) & (((key - self.start) % self.step) == 0))
                return SymbolicInteger(value, expr)
        
        return SymbolicInteger(value)
    
    def index(self, key):
        """rangeobject.index(value) -> integer -- return index of value.
        Raise ValueError if the value is not present."""
        unwrapped_key = unwrap(key)
        value = self.super.index(unwrapped_key)
        
        # 处理符号值
        if isinstance(key, SymbolicType):
            expr = (key - self.start) // self.step
            return SymbolicInteger(value, expr)
        
        return SymbolicInteger(value)