# Copyright: see copyright.txt

from .symbolic_types import SymbolicType

class ConstraintNormalizer:
    """约束规范化模块，用于将路径约束转换为规范化形式
    
    实现变量重命名、比较方向统一、常量折叠等规范化功能
    """
    
    def __init__(self):
        self.var_name_map = {}  # 变量名映射表：原始变量名 -> 标准化变量名
        self.var_counter = 0    # 标准化变量名计数器
        self.var_map_built = False  # 变量映射表是否已建立
    
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
            raw_predicates_str.append(pred.get_symbolic_expr())
            normalized_pred = self._normalize_predicate(pred)
            normalized_predicates_str.append(normalized_pred)
        
        return raw_predicates_str, normalized_predicates_str
    
    def _build_var_map(self, path_predicates):
        """建立变量映射表"""
        self.var_name_map = {}
        self.var_counter = 0
        self.var_map_built = True  # 添加标志，表示变量映射表已建立
        
        # 收集所有出现的变量，按出现顺序
        all_vars = []
        for pred in path_predicates:
            expr_str = pred.get_symbolic_expr()
            # 使用简单的方法提取变量名
            import re
            var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
            exclude = {'abs', 'not', 'and', 'or', 'True', 'False'}
            
            matches = re.findall(var_pattern, expr_str)
            for var_name in matches:
                if var_name not in exclude and var_name not in all_vars:
                    all_vars.append(var_name)
        
        # 建立变量映射
        for var_name in all_vars:
            self.var_name_map[var_name] = f'ARG{self.var_counter}'
            self.var_counter += 1
    
    def _normalize_predicate(self, predicate):
        """规范化单个谓词
        
        Args:
            predicate: Predicate对象
            
        Returns:
            str: 规范化后的谓词字符串
        """
        # 获取符号表达式
        symbolic_expr = predicate.get_symbolic_expr()
        
        # 解析表达式字符串为表达式树
        expr_tree = self._parse_expr_str(symbolic_expr)
        
        # 规范化表达式树
        normalized_tree = self.normalize_expression(expr_tree)
        
        # 考虑谓词的结果（分支方向）
        if not predicate.result:
            # 如果分支结果为 False，添加 not 操作符
            normalized_tree = ['not', normalized_tree]
        
        # 将规范化后的表达式树转换为字符串
        normalized_str = self._expr_tree_to_str(normalized_tree)
        
        return normalized_str
    
    def _parse_expr_str(self, expr_str):
        """将表达式字符串解析为表达式树
        
        Args:
            expr_str: 表达式字符串，如 "(< a 0)"
            
        Returns:
            list: 表达式树，如 ['<', 'a', 0]
        """
        expr_str = expr_str.strip()
        
        # 检查是否是简单表达式（没有括号，只是数字或变量）
        if '(' not in expr_str:
            # 尝试转换为数字
            try:
                return int(expr_str)
            except ValueError:
                try:
                    return float(expr_str)
                except ValueError:
                    return expr_str
        
        # 处理带括号的表达式
        if expr_str.startswith('(') and expr_str.endswith(')'):
            # 检查括号是否匹配
            balance = 0
            for i, char in enumerate(expr_str):
                if char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                    if balance == 0 and i == len(expr_str) - 1:
                        # 最外层括号匹配，移除它们
                        expr_str = expr_str[1:-1].strip()
                        break
        
        # 分割表达式（按空格分割，但忽略括号内的空格）
        parts = []
        current_part = ''
        depth = 0
        
        for char in expr_str:
            if char == '(':
                depth += 1
                current_part += char
            elif char == ')':
                depth -= 1
                current_part += char
            elif char == ' ' and depth == 0:
                if current_part:
                    parts.append(current_part)
                    current_part = ''
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        if not parts:
            # 尝试转换为数字
            try:
                return int(expr_str)
            except ValueError:
                try:
                    return float(expr_str)
                except ValueError:
                    return expr_str
        
        op = parts[0]
        args = parts[1:]
        
        # 递归解析参数
        parsed_args = []
        for arg in args:
            parsed_args.append(self._parse_expr_str(arg))
        
        return [op] + parsed_args
    
    def _expr_tree_to_str(self, expr_tree):
        """将表达式树转换为字符串
        
        Args:
            expr_tree: 表达式树，如 ['<', 'a', 0]
            
        Returns:
            str: 表达式字符串，如 "(< a 0)"
        """
        if isinstance(expr_tree, list):
            op = expr_tree[0]
            args = expr_tree[1:]
            args_str = ' '.join([self._expr_tree_to_str(arg) for arg in args])
            return f"({op} {args_str})"
        else:
            return str(expr_tree)
    
    def _rename_variable(self, var_name):
        """重命名变量
        
        Args:
            var_name: 原始变量名
            
        Returns:
            str: 规范化后的变量名
        """
        if var_name in self.var_name_map:
            return self.var_name_map[var_name]
        
        # 如果变量映射表已建立，不再添加新映射，返回原始变量名
        if hasattr(self, 'var_map_built') and self.var_map_built:
            return var_name
        
        # 如果变量映射表未建立，添加新的映射（用于测试等场景）
        normalized_name = f'ARG{self.var_counter}'
        self.var_name_map[var_name] = normalized_name
        self.var_counter += 1
        return normalized_name
    
    def normalize_expression(self, expr):
        """规范化表达式
        
        Args:
            expr: 表达式树，如 ['+', 'b', 'a']
            
        Returns:
            list: 规范化后的表达式树
        """
        if not isinstance(expr, list):
            # 如果是变量，重命名
            if isinstance(expr, str):
                return self._rename_variable(expr)
            return expr
        
        op = expr[0]
        args = expr[1:]
        
        # 递归规范化参数
        normalized_args = [self.normalize_expression(arg) for arg in args]
        
        # 处理不同类型的操作
        if op in ['+', '*', 'and', 'or']:
            # 对于交换律操作，对参数排序
            if op == '+' or op == '*':
                # 分离常量和变量
                constants = []
                variables = []
                for arg in normalized_args:
                    if isinstance(arg, (int, float)):
                        constants.append(arg)
                    else:
                        variables.append(arg)
                
                # 合并常量
                if constants:
                    if op == '+':
                        merged_constant = sum(constants)
                    else:  # *
                        merged_constant = 1
                        for c in constants:
                            merged_constant *= c
                    if variables:
                        variables.insert(0, merged_constant)
                    else:
                        return merged_constant
                
                # 对变量排序
                variables.sort(key=lambda x: str(x))
                return [op] + variables
            elif op == 'and' or op == 'or':
                # 对布尔操作数排序
                normalized_args.sort(key=lambda x: str(x))
                return [op] + normalized_args
        elif op in ['<', '>', '<=', '>=', '==', '!=']:
            # 规范化比较操作
            return self._normalize_comparison(op, normalized_args)
        elif op == 'not':
            # 规范化否定操作
            return [op, self.normalize_expression(normalized_args[0])]
        elif op == 'abs':
            # 规范化绝对值操作
            return [op, self.normalize_expression(normalized_args[0])]
        else:
            # 其他操作，保持不变
            return [op] + normalized_args
    
    def _merge_constants(self, op, args):
        """合并常量
        
        Args:
            op: 操作符
            args: 操作数列表
            
        Returns:
            list or int/float: 合并后的表达式或常量
        """
        constants = []
        variables = []
        
        for arg in args:
            if isinstance(arg, (int, float)):
                constants.append(arg)
            else:
                variables.append(arg)
        
        if not constants:
            return [op] + variables
        
        if op == '+':
            merged_constant = sum(constants)
        elif op == '*':
            merged_constant = 1
            for c in constants:
                merged_constant *= c
        else:
            return [op] + args
        
        if variables:
            variables.insert(0, merged_constant)
            return [op] + variables
        else:
            return merged_constant
    
    def _normalize_comparison(self, op, args):
        """规范化比较操作的方向
        
        Args:
            op: 比较操作符
            args: 操作数列表
            
        Returns:
            list: 规范化后的比较表达式
        """
        if len(args) != 2:
            return [op] + args
        
        left, right = args
        
        # 规范化比较方向
        if op == '>':
            return ['<', right, left]
        elif op == '>=':
            return ['<=', right, left]
        else:
            return [op] + args
    
    def normalize_constraint_str(self, constraint_str):
        """规范化约束字符串
        
        Args:
            constraint_str: 约束字符串
            
        Returns:
            str: 规范化后的约束字符串
        """
        # 解析表达式字符串为表达式树
        expr_tree = self._parse_expr_str(constraint_str)
        
        # 规范化表达式树
        normalized_tree = self.normalize_expression(expr_tree)
        
        # 将规范化后的表达式树转换为字符串
        normalized_str = self._expr_tree_to_str(normalized_tree)
        
        return normalized_str
