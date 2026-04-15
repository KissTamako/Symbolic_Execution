# Copyright: see copyright.txt

from .symbolic_types import SymbolicType

class ConstraintNormalizer:
    """约束规范化模块，用于将路径约束转换为规范化形式
    
    目前主要实现变量重命名功能，将输入变量统一重命名为ARG0, ARG1, ...
    """
    
    def __init__(self):
        self.var_name_map = {}  # 变量名映射表：原始变量名 -> 标准化变量名
        self.var_counter = 0    # 标准化变量名计数器
    
    def normalize_path(self, path_predicates):
        """规范化整个路径的谓词
        
        Args:
            path_predicates: 路径谓词列表
            
        Returns:
            tuple: (raw_predicates_str, normalized_predicates_str)，原始谓词字符串和规范化后的谓词字符串
        """
        # 首先建立变量映射表
        self._build_var_map(path_predicates)
        
        # 规范化每个谓词
        raw_predicates_str = []
        normalized_predicates_str = []
        
        for pred in path_predicates:
            raw_predicates_str.append(str(pred))
            normalized_pred = self._normalize_predicate(pred)
            normalized_predicates_str.append(normalized_pred)
        
        return raw_predicates_str, normalized_predicates_str
    
    def _build_var_map(self, path_predicates):
        """建立变量映射表"""
        self.var_name_map = {}
        self.var_counter = 0
        
        # 收集所有变量名，按顺序建立映射
        for pred in path_predicates:
            vars_in_pred = pred.getVars()
            for var_name in vars_in_pred:
                if var_name not in self.var_name_map:
                    self.var_name_map[var_name] = f'ARG{self.var_counter}'
                    self.var_counter += 1
    
    def _normalize_predicate(self, predicate):
        """规范化单个谓词
        
        Args:
            predicate: Predicate对象
            
        Returns:
            str: 规范化后的谓词字符串
        """
        # 获取原始谓词字符串
        pred_str = str(predicate)
        
        # 替换变量名
        normalized_str = pred_str
        for original_name, normalized_name in self.var_name_map.items():
            # 只替换完整的变量名，避免部分匹配
            # 使用简单的字符串替换，后面可以改进为更精确的方法
            normalized_str = normalized_str.replace(original_name, normalized_name)
        
        return normalized_str
    
    def normalize_constraint_str(self, constraint_str):
        """规范化约束字符串
        
        Args:
            constraint_str: 约束字符串
            
        Returns:
            str: 规范化后的约束字符串
        """
        # 这个方法主要用于后续扩展
        # 目前主要通过 normalize_path 来规范化整个路径
        return constraint_str
