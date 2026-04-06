#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用学生代码分析器
面向学生代码的增强型符号执行工具 - 核心分析模块

功能：
1. 分析学生代码的结构特征
2. 识别输入点和输出点
3. 提取控制流特征
4. 检测常见错误模式
5. 生成代码特征向量
"""

import ast
import re
import sys
from typing import Dict, List, Any, Optional, Tuple
import inspect


class UniversalCodeAnalyzer:
    """通用学生代码分析器"""
    
    def __init__(self, code: str):
        """
        初始化分析器
        
        Args:
            code: 学生代码字符串
        """
        self.code = code
        self.ast_tree = None
        self.features = {}
        self.errors = []
        
    def analyze(self) -> Dict[str, Any]:
        """
        执行完整代码分析
        
        Returns:
            包含所有分析特征的字典
        """
        try:
            # 解析代码为AST
            self.ast_tree = ast.parse(self.code)
            
            # 提取基本特征
            self._extract_basic_features()
            
            # 分析函数定义
            self._analyze_functions()
            
            # 分析控制流
            self._analyze_control_flow()
            
            # 分析输入输出
            self._analyze_input_output()
            
            # 检测常见错误模式
            self._detect_error_patterns()
            
            # 生成特征向量
            self._generate_feature_vector()
            
            return {
                "success": True,
                "features": self.features,
                "errors": self.errors,
                "code_type": self._classify_code_type(),
                "recommendations": self._generate_recommendations()
            }
            
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"语法错误: {e}",
                "line": e.lineno,
                "offset": e.offset
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"分析错误: {e}"
            }
    
    def _extract_basic_features(self):
        """提取基本代码特征"""
        # 代码行数统计
        lines = self.code.split('\n')
        self.features['line_count'] = len(lines)
        self.features['non_empty_line_count'] = len([l for l in lines if l.strip()])
        
        # 统计注释行数
        comment_lines = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                comment_lines += 1
        self.features['comment_line_count'] = comment_lines
        
        # 代码复杂度指标
        self.features['import_count'] = len([n for n in ast.walk(self.ast_tree) if isinstance(n, ast.Import)])
        self.features['import_from_count'] = len([n for n in ast.walk(self.ast_tree) if isinstance(n, ast.ImportFrom)])
    
    def _analyze_functions(self):
        """分析函数定义"""
        functions = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': len(node.args.args),
                    'defaults': len(node.args.defaults),
                    'decorators': len(node.decorator_list),
                    'has_return': any(isinstance(n, ast.Return) for n in ast.walk(node)),
                    'has_docstring': ast.get_docstring(node) is not None
                }
                functions.append(func_info)
        
        self.features['function_count'] = len(functions)
        self.features['functions'] = functions
        
        # 检测是否有main函数
        has_main = any(f['name'] == 'main' for f in functions)
        self.features['has_main_function'] = has_main
        
        # 检测是否有特定函数名模式
        prime_functions = ['sushu', 'isPrime', 'isprime', 'prime']
        palindrome_functions = ['huiwen', 'huiwenshu', 'huiwensushu', 'reverseNumber', 'reverse']
        
        prime_func_count = sum(1 for f in functions if any(p in f['name'].lower() for p in prime_functions))
        palindrome_func_count = sum(1 for f in functions if any(p in f['name'].lower() for p in palindrome_functions))
        
        self.features['prime_function_count'] = prime_func_count
        self.features['palindrome_function_count'] = palindrome_func_count
    
    def _analyze_control_flow(self):
        """分析控制流特征"""
        loop_count = 0
        if_count = 0
        try_count = 0
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
                loop_count += 1
            elif isinstance(node, ast.If):
                if_count += 1
            elif isinstance(node, ast.Try):
                try_count += 1
        
        self.features['loop_count'] = loop_count
        self.features['if_count'] = if_count
        self.features['try_count'] = try_count
        
        # 计算最大嵌套深度
        self.features['max_nesting_depth'] = self._calculate_max_nesting_depth()
    
    def _calculate_max_nesting_depth(self) -> int:
        """计算最大嵌套深度"""
        max_depth = 0
        current_depth = 0
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                # 函数定义重置深度
                pass
            elif isinstance(node, (ast.For, ast.While, ast.If, ast.Try, ast.With, ast.AsyncFor, ast.AsyncWith)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        
        return max_depth
    
    def _analyze_input_output(self):
        """分析输入输出特征"""
        # 查找input()调用
        input_calls = []
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'input':
                    input_calls.append(ast.unparse(node))
        
        self.features['input_call_count'] = len(input_calls)
        self.features['input_calls'] = input_calls
        
        # 查找print()调用
        print_calls = []
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'print':
                    print_calls.append(ast.unparse(node))
        
        self.features['print_call_count'] = len(print_calls)
        self.features['print_calls'] = print_calls
        
        # 检测eval()使用
        eval_calls = []
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                    eval_calls.append(ast.unparse(node))
        
        self.features['eval_call_count'] = len(eval_calls)
        self.features['eval_calls'] = eval_calls
        
        # 检测是否有直接执行代码（无函数定义）
        has_global_code = False
        for node in self.ast_tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
                has_global_code = True
                break
        
        self.features['has_global_code'] = has_global_code
    
    def _detect_error_patterns(self):
        """检测常见错误模式"""
        error_patterns = []
        
        # 1. 检查无限循环风险
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.While):
                # 检查while循环条件是否为常量True
                if isinstance(node.test, ast.Constant) and node.test.value is True:
                    error_patterns.append({
                        'type': 'potential_infinite_loop',
                        'line': node.lineno,
                        'message': 'while True可能导致无限循环，缺乏break语句'
                    })
        
        # 2. 检查可能的除零错误
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                # 检查除数是否可能为0
                if isinstance(node.right, ast.Constant) and node.right.value == 0:
                    error_patterns.append({
                        'type': 'division_by_zero',
                        'line': node.lineno,
                        'message': '除数为0可能导致运行时错误'
                    })
        
        # 3. 检查未处理的异常
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                # 检查危险函数调用
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in ['open', 'eval', 'exec'] and not self._is_in_try_block(node):
                        error_patterns.append({
                            'type': 'unhandled_exception_risk',
                            'line': node.lineno,
                            'message': f'{func_name}()调用可能引发异常，建议添加异常处理'
                        })
        
        self.features['error_patterns'] = error_patterns
        self.features['error_count'] = len(error_patterns)
    
    def _is_in_try_block(self, node: ast.AST) -> bool:
        """检查节点是否在try块中"""
        current = node
        while hasattr(current, 'parent'):
            if isinstance(current.parent, ast.Try):
                return True
            current = current.parent
        return False
    
    def _generate_feature_vector(self):
        """生成数值特征向量"""
        feature_vector = [
            self.features.get('line_count', 0),
            self.features.get('function_count', 0),
            self.features.get('loop_count', 0),
            self.features.get('if_count', 0),
            self.features.get('try_count', 0),
            self.features.get('input_call_count', 0),
            self.features.get('print_call_count', 0),
            self.features.get('eval_call_count', 0),
            self.features.get('prime_function_count', 0),
            self.features.get('palindrome_function_count', 0),
            self.features.get('max_nesting_depth', 0),
            int(self.features.get('has_main_function', False)),
            int(self.features.get('has_global_code', False)),
            self.features.get('error_count', 0)
        ]
        
        self.features['feature_vector'] = feature_vector
    
    def _classify_code_type(self) -> str:
        """基于特征进行代码类型分类"""
        prime_func_count = self.features.get('prime_function_count', 0)
        palindrome_func_count = self.features.get('palindrome_function_count', 0)
        
        if prime_func_count > 0 and palindrome_func_count > 0:
            return 'prime_palindrome'
        elif prime_func_count > 0:
            return 'prime_only'
        elif palindrome_func_count > 0:
            return 'palindrome_only'
        elif self.features.get('function_count', 0) == 0 and self.features.get('has_global_code', False):
            return 'script_no_functions'
        else:
            return 'unknown'
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于分析结果生成建议
        if self.features.get('function_count', 0) == 0:
            recommendations.append("代码中没有定义函数，建议将主要逻辑封装到函数中")
        
        if self.features.get('has_global_code', False) and self.features.get('function_count', 0) > 0:
            recommendations.append("代码包含全局执行语句和函数定义，建议将全局逻辑移到main()函数中")
        
        if self.features.get('try_count', 0) == 0 and self.features.get('input_call_count', 0) > 0:
            recommendations.append("代码使用input()但没有异常处理，建议添加try-except块处理用户输入")
        
        if self.features.get('comment_line_count', 0) < 3:
            recommendations.append("代码注释较少，建议添加必要的文档注释")
        
        error_patterns = self.features.get('error_patterns', [])
        for error in error_patterns:
            recommendations.append(f"第{error['line']}行: {error['message']}")
        
        return recommendations


# ========== 使用示例和测试 ==========

def analyze_example_code():
    """示例代码分析"""
    example_code = '''
def sushu(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def huiwenshu(n):
    return str(n) == str(n)[::-1]

n = int(input("请输入N: "))
result = []
for i in range(2, n+1):
    if sushu(i) and huiwenshu(i):
        result.append(i)
print(result)
'''
    
    analyzer = UniversalCodeAnalyzer(example_code)
    result = analyzer.analyze()
    
    print("代码分析结果:")
    print("=" * 60)
    print(f"分析成功: {result['success']}")
    print(f"代码类型: {result['code_type']}")
    print(f"函数数量: {result['features']['function_count']}")
    print(f"循环数量: {result['features']['loop_count']}")
    print(f"条件数量: {result['features']['if_count']}")
    print(f"输入调用: {result['features']['input_call_count']}")
    print(f"错误数量: {result['features']['error_count']}")
    print()
    print("特征向量:", result['features']['feature_vector'])
    print()
    print("改进建议:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"  {i}. {rec}")


if __name__ == "__main__":
    analyze_example_code()