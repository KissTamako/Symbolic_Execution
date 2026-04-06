"""SymbolicList - 符号列表类型支持框架

这个模块提供列表类型的符号执行支持。
目前是框架实现，需要进一步开发完整的符号列表功能。
"""

from . symbolic_type import SymbolicObject
from .symbolic_int import SymbolicInteger

class SymbolicList(SymbolicObject, list):
    """符号列表类型 - 支持列表的符号执行
    
    这是一个框架实现，需要进一步完善以下功能：
    1. 列表索引访问的符号表达式
    2. 列表切片操作的符号支持
    3. 列表方法的符号实现（append, extend, pop等）
    4. 列表长度的符号表示
    """
    
    def __new__(cls, name, *args, **kwargs):
        """创建新的符号列表实例"""
        self = list.__new__(cls, *args, **kwargs)
        return self
    
    def __init__(self, name, v, expr=None):
        """初始化符号列表
        
        参数:
            name: 变量名
            v: 具体列表值
            expr: 符号表达式（可选）
        """
        SymbolicObject.__init__(self, name, expr)
        list.__init__(self, v)
        self.val = v
    
    def getConcrValue(self):
        """获取具体值"""
        return self.val
    
    def wrap(conc, sym):
        """包装具体值和符号表达式为SymbolicList
        
        参数:
            conc: 具体列表值
            sym: 符号表达式
        
        返回:
            SymbolicList实例
        """
        return SymbolicList("se", conc, sym)
    
    @classmethod
    def _wrap_none(cls, conc, sym):
        """包装None值和符号表达式
        list.append()返回None，但我们需要生成符号表达式
        """
        # 创建一个特殊的SymbolicNone类型，或者返回SymbolicInteger包装的0
        # 这里简化处理：返回SymbolicInteger包装的0
        from .symbolic_int import SymbolicInteger
        return SymbolicInteger.wrap(0, sym)
    
    def __len__(self):
        """获取列表长度 - 符号支持"""
        # 使用符号表达式生成列表长度
        return self._do_sexpr([self], lambda x: len(x.val) if hasattr(x, 'val') else len(x), "list.len", SymbolicInteger.wrap)
    
    def __getitem__(self, key):
        """获取列表元素 - 符号支持"""
        # 使用符号表达式生成索引访问
        return self._do_sexpr([self, key], 
            lambda x, k: x.val[k] if hasattr(x, 'val') else x[k] if isinstance(x, list) else 0,
            "list.getitem", 
            SymbolicInteger.wrap)
    
    def __setitem__(self, key, value):
        """设置列表元素 - 符号支持"""
        # 更新具体值
        self.val[key] = value
        # 生成符号设置表达式
        return self._do_sexpr([self, key, value], 
            lambda x, k, v: x.val[k] if hasattr(x, 'val') else (x[k] if isinstance(x, list) else None),
            "list.setitem",
            SymbolicList.wrap)
    
    def __contains__(self, item):
        """检查是否包含元素 - 符号支持"""
        # 使用符号表达式生成包含检查
        return self._do_sexpr([self, item], 
            lambda x, i: i in x.val if hasattr(x, 'val') else (i in x if isinstance(x, list) else False),
            "list.contains", 
            SymbolicInteger.wrap)
    
    def append(self, item):
        """添加元素到列表末尾 - 符号支持"""
        # 更新具体值
        self.val.append(item)
        # 生成符号追加表达式
        # 注意：list.append返回None，但我们需要生成符号表达式
        # 返回None的包装版本
        return self._do_sexpr([self, item], 
            lambda x, i: None,  # 具体操作返回None
            "list.append", 
            lambda conc, sym: self._wrap_none(conc, sym))
    
    def extend(self, iterable):
        """扩展列表 - 符号支持"""
        # 更新具体值
        self.val.extend(iterable)
        # 生成符号扩展表达式
        # 注意：list.extend返回None，但我们需要生成符号表达式
        return self._do_sexpr([self, iterable], 
            lambda x, i: None,  # 具体操作返回None
            "list.extend", 
            lambda conc, sym: self._wrap_none(conc, sym))
    
    def pop(self, index=-1):
        """移除并返回元素 - 符号支持"""
        # 更新具体值并获取被移除的元素
        removed = self.val.pop(index)
        # 生成符号弹出表达式
        # 返回被移除元素的符号表示
        # 注意：lambda函数应该返回被移除的元素值，而不是再次调用pop
        return self._do_sexpr([self, index], 
            lambda x, i: removed,  # 使用已经弹出的具体值
            "list.pop", 
            SymbolicInteger.wrap)
    
    def insert(self, index, item):
        """插入元素 - 符号支持"""
        # 更新具体值
        self.val.insert(index, item)
        # 生成符号插入表达式
        # 注意：list.insert返回None，但我们需要生成符号表达式
        return self._do_sexpr([self, index, item], 
            lambda x, i, v: None,  # 具体操作返回None
            "list.insert", 
            lambda conc, sym: self._wrap_none(conc, sym))
    
    def remove(self, item):
        """移除元素 - 符号支持"""
        # 更新具体值（如果元素不存在会引发ValueError）
        self.val.remove(item)
        # 生成符号移除表达式
        # 注意：list.remove返回None，但我们需要生成符号表达式
        return self._do_sexpr([self, item], 
            lambda x, i: None,  # 具体操作返回None
            "list.remove", 
            lambda conc, sym: self._wrap_none(conc, sym))
    
    def count(self, item):
        """统计元素出现次数 - 符号支持"""
        # 使用符号表达式生成计数操作
        return self._do_sexpr([self, item], 
            lambda x, i: x.val.count(i) if hasattr(x, 'val') else (x.count(i) if isinstance(x, list) else 0),
            "list.count", 
            SymbolicInteger.wrap)
    
    def index(self, item, start=0, end=None):
        """查找元素索引 - 符号支持"""
        # 使用符号表达式生成索引查找操作
        return self._do_sexpr([self, item, start, end if end is not None else len(self.val)], 
            lambda x, i, s, e: x.val.index(i, s, e) if hasattr(x, 'val') else (x.index(i, s, e) if isinstance(x, list) else -1),
            "list.index", 
            SymbolicInteger.wrap)
    
    def sort(self, key=None, reverse=False):
        """排序列表 - 符号支持（简化版本）"""
        # 排序操作对符号执行非常复杂，特别是key函数可能是符号函数
        # 我们实现一个简化版本：对具体值排序，生成符号表达式
        # 更新具体值
        self.val.sort(key=key, reverse=reverse)
        # 生成符号排序表达式
        # 注意：list.sort返回None，但我们需要生成符号表达式
        # 简化处理：如果key是None，生成简单表达式；否则记录复杂操作
        if key is None:
            return self._do_sexpr([self, reverse], 
                lambda x, r: None,  # 具体操作返回None
                "list.sort", 
                lambda conc, sym: self._wrap_none(conc, sym))
        else:
            # key函数可能复杂，简化处理
            return self._do_sexpr([self, key, reverse], 
                lambda x, k, r: None,  # 具体操作返回None
                "list.sort_with_key", 
                lambda conc, sym: self._wrap_none(conc, sym))
    
    def reverse(self):
        """反转列表 - 符号支持"""
        # 更新具体值
        self.val.reverse()
        # 生成符号反转表达式
        # 注意：list.reverse返回None，但我们需要生成符号表达式
        return self._do_sexpr([self], 
            lambda x: None,  # 具体操作返回None
            "list.reverse", 
            lambda conc, sym: self._wrap_none(conc, sym))
    
    def copy(self):
        """复制列表 - 符号支持"""
        # 生成符号复制表达式
        return self._do_sexpr([self], 
            lambda x: x.val.copy() if hasattr(x, 'val') else x.copy() if isinstance(x, list) else [],
            "list.copy", 
            SymbolicList.wrap)
    
    def clear(self):
        """清空列表 - 符号支持"""
        # 更新具体值
        self.val.clear()
        # 生成符号清空表达式
        # 注意：list.clear返回None，但我们需要生成符号表达式
        return self._do_sexpr([self], 
            lambda x: None,  # 具体操作返回None
            "list.clear", 
            lambda conc, sym: self._wrap_none(conc, sym))
    
    # 需要实现的符号操作方法
    def _op_worker(self, args, fun, op):
        """符号操作工作器"""
        # 生成符号表达式
        return self._do_sexpr(args, fun, op, SymbolicList.wrap)
