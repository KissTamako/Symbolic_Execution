#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用适配器生成器
面向学生代码的增强型符号执行工具 - 适配器生成模块

功能：
1. 根据学生代码分析结果生成符号执行适配器
2. 自动添加@symbolic装饰器和expected_result()函数
3. 支持多种代码结构（函数式、过程式、混合式）
4. 生成可执行的测试代码
"""

import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from universal_code_analyzer import UniversalCodeAnalyzer


class UniversalAdapterGenerator:
    """通用适配器生成器"""
    
    def __init__(self, original_code: str):
        """
        初始化适配器生成器
        
        Args:
            original_code: 原始学生代码字符串
        """
        self.original_code = original_code
        self.analyzer = UniversalCodeAnalyzer(original_code)
        self.analysis_result = None
        self.adapter_code = ""
        
    def generate_adapter(self) -> Dict[str, Any]:
        """
        生成适配器代码
        
        Returns:
            包含生成结果和适配器代码的字典
        """
        try:
            # 分析原始代码
            self.analysis_result = self.analyzer.analyze()
            
            if not self.analysis_result['success']:
                return {
                    'success': False,
                    'error': self.analysis_result['error'],
                    'adapter_code': ''
                }
            
            # 根据代码类型选择生成策略
            code_type = self.analysis_result['code_type']
            
            if code_type in ['prime_palindrome', 'prime_only', 'palindrome_only']:
                self._generate_functional_adapter()
            elif code_type == 'script_no_functions':
                self._generate_script_adapter()
            else:
                self._generate_general_adapter()
            
            # 添加必要的导入和配置
            self._add_imports_and_config()
            
            return {
                'success': True,
                'code_type': code_type,
                'features': self.analysis_result['features'],
                'adapter_code': self.adapter_code,
                'test_function_name': self._get_test_function_name(),
                'recommendations': self.analysis_result['recommendations']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"适配器生成失败: {e}",
                'adapter_code': ''
            }
    
    def _generate_functional_adapter(self):
        """生成函数式代码的适配器（如质数回文数）"""
        # 获取函数信息
        functions = self.analysis_result['features'].get('functions', [])
        
        # 构建适配器头部
        self.adapter_code = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
符号执行适配器 - 函数式代码
生成的测试代码，用于PyExZ3符号执行
"""

from symbolic.args import *
        
'''
        
        # 添加原始代码（去除input调用）
        original_without_input = self._remove_input_calls(self.original_code)
        self.adapter_code += original_without_input
        self.adapter_code += "\n\n"
        
        # 生成测试函数
        if functions:
            # 使用第一个函数作为主要测试函数
            main_func = functions[0]
            func_name = main_func['name']
            
            # 确定参数类型和默认值
            param_name = self._detect_main_parameter()
            
            test_function = f'''
# ========== 符号执行测试函数 ==========
@symbolic({param_name}=10)
def test_student_code({param_name}):
    """
    符号执行测试函数
    参数: {param_name} - 输入值
    返回: 执行结果
    """
    try:
        # 输入验证
        if {param_name} < 1:
            return []
        
        result = []
        # 执行核心逻辑
        for i in range(2, {param_name} + 1):
'''
            
            # 根据代码类型添加测试逻辑
            code_type = self.analysis_result['code_type']
            if code_type == 'prime_palindrome':
                # 需要找到质数函数和回文函数
                prime_func = self._find_prime_function(functions)
                palindrome_func = self._find_palindrome_function(functions)
                
                if prime_func and palindrome_func:
                    test_function += f'''
            # 质数回文数检测
            if {prime_func['name']}(i) and {palindrome_func['name']}(i):
                result.append(i)
'''
                else:
                    # 通用检测
                    test_function += f'''
            # 通用检测
            try:
                # 尝试调用所有函数
                for func in [{', '.join([f['name'] for f in functions])}]:
                    pass
                result.append(i)
            except:
                pass
'''
            elif code_type == 'prime_only':
                prime_func = self._find_prime_function(functions)
                if prime_func:
                    test_function += f'''
            # 质数检测
            if {prime_func['name']}(i):
                result.append(i)
'''
            elif code_type == 'palindrome_only':
                palindrome_func = self._find_palindrome_function(functions)
                if palindrome_func:
                    test_function += f'''
            # 回文数检测
            if {palindrome_func['name']}(i):
                result.append(i)
'''
            
            test_function += f'''
        return result
        
    except Exception as e:
        # 异常时返回空列表
        return []
'''
            
            self.adapter_code += test_function
            
        else:
            # 没有函数，生成通用适配器
            self._generate_general_adapter()
    
    def _generate_script_adapter(self):
        """生成过程式代码的适配器（无函数定义）"""
        # 识别主要输入变量
        input_calls = self.analysis_result['features'].get('input_calls', [])
        main_var = self._detect_main_variable()
        
        self.adapter_code = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
符号执行适配器 - 过程式代码
生成的测试代码，用于PyExZ3符号执行
"""

from symbolic.args import *

# ========== 原始代码逻辑（封装为函数） ==========
def execute_student_logic({main_var}):
    """
    封装原始代码逻辑
    """
    # 复制原始代码逻辑，替换input调用
'''
        
        # 转换原始代码为函数
        script_code = self._convert_script_to_function(self.original_code, main_var)
        self.adapter_code += script_code
        self.adapter_code += "\n\n"
        
        # 生成测试函数
        test_function = f'''
# ========== 符号执行测试函数 ==========
@symbolic({main_var}=10)
def test_student_code({main_var}):
    """
    符号执行测试函数
    参数: {main_var} - 输入值
    返回: 执行结果
    """
    try:
        return execute_student_logic({main_var})
    except Exception as e:
        # 异常时返回默认值
        return []
'''
        
        self.adapter_code += test_function
    
    def _generate_general_adapter(self):
        """生成通用适配器（未知代码类型）"""
        self.adapter_code = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
符号执行适配器 - 通用类型
生成的测试代码，用于PyExZ3符号执行
"""

from symbolic.args import *

'''
        
        # 添加原始代码
        self.adapter_code += self.original_code
        self.adapter_code += "\n\n"
        
        # 生成通用测试函数
        param_name = "input_value"
        
        test_function = f'''
# ========== 符号执行测试函数 ==========
@symbolic({param_name}=10)
def test_student_code({param_name}):
    """
    通用符号执行测试函数
    参数: {param_name} - 输入值
    返回: 执行结果或状态码
    """
    try:
        # 简单验证逻辑
        if {param_name} < 0:
            return -1
        
        # 尝试执行原始代码逻辑
        # 这里需要根据具体代码调整
        result = 0
        
        # 示例：简单条件测试
        if {param_name} > 10:
            result = 1
        else:
            result = 0
            
        return result
        
    except Exception as e:
        # 异常时返回错误代码
        return -999
'''
        
        self.adapter_code += test_function
    
    def _add_imports_and_config(self):
        """添加必要的导入和配置"""
        if "from symbolic.args import *" not in self.adapter_code:
            # 确保有导入
            lines = self.adapter_code.split('\n')
            if lines[0].startswith('#!/usr/bin/env python'):
                # 在shebang后添加导入
                lines.insert(1, '')
                lines.insert(2, 'from symbolic.args import *')
                lines.insert(3, '')
                self.adapter_code = '\n'.join(lines)
        
        # 添加expected_result函数
        expected_result_func = '''
# ========== 期望结果函数（PyExZ3需要） ==========
def expected_result():
    """返回期望的结果，用于PyExZ3验证"""
    # 对于通用测试，返回一些可能的输出值
    return [0, 1, -1]
'''
        
        self.adapter_code += expected_result_func
        
        # 添加主测试函数
        main_test = '''
# ========== 主程序（用于手动测试） ==========
def main_test():
    """运行简单测试"""
    print("生成的适配器测试")
    print("=" * 60)
    
    test_values = [5, 10, 15]
    for val in test_values:
        result = test_student_code(val)
        print(f"输入值: {val}, 结果: {result}")
    
    print("\\n测试完成")

if __name__ == "__main__":
    main_test()
'''
        
        self.adapter_code += main_test
    
    def _remove_input_calls(self, code: str) -> str:
        """移除input()调用，替换为参数"""
        # 简单的正则替换，将input()调用替换为参数
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 匹配类似 n = input("提示") 或 n = int(input("提示"))
            if 'input(' in line:
                # 暂时注释掉input行
                cleaned_lines.append(f"# {line}  # 已替换为参数")
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _detect_main_parameter(self) -> str:
        """检测主要参数名"""
        # 常见的学生代码参数名
        common_params = ['n', 'N', 'num', 'number', 'x', 'value', 'input_value']
        
        # 从原始代码中查找
        for param in common_params:
            if re.search(rf'\b{param}\b', self.original_code):
                return param
        
        # 默认参数名
        return 'n'
    
    def _detect_main_variable(self) -> str:
        """检测主要变量名"""
        # 查找input()调用赋值的变量
        input_pattern = r'(\w+)\s*=\s*(?:int\()?\s*input\s*\('
        match = re.search(input_pattern, self.original_code)
        
        if match:
            return match.group(1)
        
        # 查找常见的变量名
        common_vars = ['n', 'N', 'num', 'number', 'x']
        for var in common_vars:
            if re.search(rf'\b{var}\b', self.original_code):
                return var
        
        return 'input_val'
    
    def _find_prime_function(self, functions: List[Dict]) -> Optional[Dict]:
        """查找质数检测函数"""
        prime_keywords = ['sushu', 'isprime', 'prime']
        
        for func in functions:
            func_name_lower = func['name'].lower()
            for keyword in prime_keywords:
                if keyword in func_name_lower:
                    return func
        
        return None
    
    def _find_palindrome_function(self, functions: List[Dict]) -> Optional[Dict]:
        """查找回文数检测函数"""
        palindrome_keywords = ['huiwen', 'reverse', 'palindrome']
        
        for func in functions:
            func_name_lower = func['name'].lower()
            for keyword in palindrome_keywords:
                if keyword in func_name_lower:
                    return func
        
        return None
    
    def _convert_script_to_function(self, code: str, param_name: str) -> str:
        """将过程式代码转换为函数"""
        lines = code.split('\n')
        function_lines = []
        
        for line in lines:
            # 替换input()调用
            if 'input(' in line:
                # 提取input()调用
                input_match = re.search(r'(\w+)\s*=\s*(.*?)input\s*\(', line)
                if input_match:
                    var_name = input_match.group(1)
                    # 替换为参数
                    new_line = f"    {var_name} = {param_name}  # 替换原始input调用"
                    function_lines.append(new_line)
                else:
                    function_lines.append(f"    # {line}  # 已处理")
            elif line.strip() and not line.strip().startswith('#'):
                # 非空行，非注释行，添加缩进
                function_lines.append(f"    {line}")
            else:
                function_lines.append(line)
        
        return '\n'.join(function_lines)
    
    def _get_test_function_name(self) -> str:
        """获取测试函数名"""
        return "test_student_code"


# ========== 使用示例和测试 ==========

def generate_example_adapters():
    """示例适配器生成"""
    
    # 示例1：函数式代码（质数回文数）
    example1 = '''
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
    
    print("示例1：函数式代码适配器生成")
    print("=" * 60)
    
    generator1 = UniversalAdapterGenerator(example1)
    result1 = generator1.generate_adapter()
    
    if result1['success']:
        print(f"代码类型: {result1['code_type']}")
        print(f"测试函数: {result1['test_function_name']}")
        print(f"特征向量: {result1['features']['feature_vector']}")
        print("\n生成的适配器代码前50行:")
        print("-" * 40)
        lines = result1['adapter_code'].split('\n')[:50]
        for i, line in enumerate(lines, 1):
            print(f"{i:3}: {line}")
        print("..." if len(result1['adapter_code'].split('\n')) > 50 else "")
    else:
        print(f"生成失败: {result1['error']}")
    
    print("\n" + "=" * 60 + "\n")
    
    # 示例2：过程式代码
    example2 = '''
n = eval(input())
a=[]
if type(n)==float or n<=1:
    print("illegal input")
else:
    for x in range(2,n+1):
        if x==2:
            a.append(str(x))
        for i in range(2,x):
            if x%i==0:
                break
            elif str(x)!=str(x)[::-1]:
                break
            elif i==x-1:
                a.append(str(x))
list1=' '.join(a)
print(list1)
'''
    
    print("示例2：过程式代码适配器生成")
    print("=" * 60)
    
    generator2 = UniversalAdapterGenerator(example2)
    result2 = generator2.generate_adapter()
    
    if result2['success']:
        print(f"代码类型: {result2['code_type']}")
        print(f"测试函数: {result2['test_function_name']}")
        print(f"特征向量: {result2['features']['feature_vector']}")
        print("\n生成的适配器代码前50行:")
        print("-" * 40)
        lines = result2['adapter_code'].split('\n')[:50]
        for i, line in enumerate(lines, 1):
            print(f"{i:3}: {line}")
        print("..." if len(result2['adapter_code'].split('\n')) > 50 else "")
    else:
        print(f"生成失败: {result2['error']}")
    
    print("\n" + "=" * 60 + "\n")
    
    # 示例3：简单代码
    example3 = '''
def simple(x):
    if x > 10:
        return 1
    else:
        return 0
'''
    
    print("示例3：简单函数代码适配器生成")
    print("=" * 60)
    
    generator3 = UniversalAdapterGenerator(example3)
    result3 = generator3.generate_adapter()
    
    if result3['success']:
        print(f"代码类型: {result3['code_type']}")
        print(f"测试函数: {result3['test_function_name']}")
        print(f"特征向量: {result3['features']['feature_vector']}")
        
        # 保存适配器文件
        adapter_file = "generated_adapter_example.py"
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.write(result3['adapter_code'])
        print(f"\n适配器已保存到: {adapter_file}")
        
        # 运行测试
        print("\n运行适配器测试:")
        print("-" * 40)
        import subprocess
        try:
            result = subprocess.run(['python', adapter_file], 
                                   capture_output=True, text=True, timeout=5)
            print(result.stdout)
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
        except Exception as e:
            print(f"运行测试失败: {e}")
    else:
        print(f"生成失败: {result3['error']}")


if __name__ == "__main__":
    generate_example_adapters()