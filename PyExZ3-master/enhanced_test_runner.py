#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强版符号执行测试运行器
解决编码问题和测试函数名检测问题
"""

import subprocess
import os
import time
import re
import json
from typing import Dict, List, Any, Optional


class EnhancedTestRunner:
    """增强版测试运行器，解决编码和函数名检测问题"""
    
    def __init__(self, pyexz3_path: str = "pyexz3.py"):
        self.pyexz3_path = pyexz3_path
        self.results = []
    
    def detect_test_function(self, adapter_file: str) -> Optional[str]:
        """检测适配器文件中的测试函数名"""
        try:
            with open(adapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找@symbolic装饰的函数
            symbolic_pattern = r'@symbolic\s*\(.*?\)\s*\n\s*def\s+(\w+)\s*\('
            match = re.search(symbolic_pattern, content, re.DOTALL)
            if match:
                return match.group(1)
            
            # 查找包含"test"的函数名
            test_pattern = r'def\s+(test_\w+)\s*\('
            match = re.search(test_pattern, content)
            if match:
                return match.group(1)
            
            # 对于PyExZ3官方测试，函数名通常是文件名
            base_name = os.path.basename(adapter_file).replace('.py', '')
            return base_name
            
        except Exception:
            return "test_student_code"  # 默认值
    
    def run_test(self, adapter_file: str, test_function: Optional[str] = None,
                max_iters: int = 5, use_z3: bool = True, timeout: int = 30) -> Dict[str, Any]:
        """运行符号执行测试，处理编码问题"""
        start_time = time.time()
        
        # 自动检测测试函数名
        if test_function is None:
            test_function = self.detect_test_function(adapter_file)
        
        try:
            # 构建命令
            cmd = [
                "python", self.pyexz3_path,
                f"--max-iters={max_iters}",
                f"--start={test_function}"
            ]
            
            if use_z3:
                cmd.append("--z3")
            
            cmd.append(adapter_file)
            
            # 运行命令，使用更健壮的方式处理编码
            process = subprocess.run(
                cmd,
                capture_output=True,
                timeout=timeout,
                text=True,
                encoding='utf-8',
                errors='replace'  # 替换无法解码的字符
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 分析输出
            output = process.stdout
            error_output = process.stderr
            
            # 解析结果
            test_passed = "test passed" in output or "test passed" in output.lower()
            paths_explored = self._extract_paths_count(output)
            
            result = {
                'success': process.returncode == 0,
                'test_passed': test_passed,
                'return_code': process.returncode,
                'execution_time': execution_time,
                'paths_explored': paths_explored,
                'output': output,
                'error_output': error_output,
                'command': ' '.join(cmd),
                'adapter_file': adapter_file,
                'test_function': test_function,
                'detected_function': self.detect_test_function(adapter_file)
            }
            
            self.results.append(result)
            return result
            
        except subprocess.TimeoutExpired:
            end_time = time.time()
            return {
                'success': False,
                'test_passed': False,
                'return_code': -1,
                'execution_time': end_time - start_time,
                'paths_explored': 0,
                'output': '',
                'error_output': f"测试超时 ({timeout}秒)",
                'command': '',
                'adapter_file': adapter_file,
                'test_function': test_function,
                'timeout': True
            }
        except Exception as e:
            end_time = time.time()
            return {
                'success': False,
                'test_passed': False,
                'return_code': -1,
                'execution_time': end_time - start_time,
                'paths_explored': 0,
                'output': '',
                'error_output': f"执行异常: {str(e)}",
                'command': '',
                'adapter_file': adapter_file,
                'test_function': test_function
            }
    
    def _extract_paths_count(self, output: str) -> int:
        """提取路径探索数量"""
        patterns = [
            r'Explored\s+(\d+)\s+paths',
            r'探索了\s*(\d+)\s*条路径',
            r'paths?\s*:\s*(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # 尝试从输出行中提取
        lines = output.split('\n')
        for line in lines:
            if 'path' in line.lower() or '路径' in line:
                numbers = re.findall(r'\d+', line)
                if numbers:
                    return int(numbers[0])
        
        return 0
    
    def run_direct_pyexz3_test(self, adapter_file: str) -> Dict[str, Any]:
        """直接运行PyExZ3测试，不使用subprocess捕获，避免编码问题"""
        print(f"\n直接运行PyExZ3测试: {adapter_file}")
        print("=" * 60)
        
        # 直接打印命令，让用户看到输出
        test_function = self.detect_test_function(adapter_file)
        cmd = f'python {self.pyexz3_path} --z3 --max-iters=5 --start={test_function} {adapter_file}'
        print(f"命令: {cmd}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # 使用os.system直接运行，避免编码问题
            return_code = os.system(cmd)
            end_time = time.time()
            
            result = {
                'success': return_code == 0,
                'return_code': return_code,
                'execution_time': end_time - start_time,
                'adapter_file': adapter_file,
                'test_function': test_function,
                'method': 'direct_os_system'
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'adapter_file': adapter_file,
                'test_function': test_function
            }


def test_basic_pyexz3():
    """测试基本PyExZ3功能"""
    print("测试基本PyExZ3功能")
    print("=" * 60)
    
    # 测试官方示例
    if os.path.exists("test/simple.py"):
        print("1. 测试官方示例: test/simple.py")
        runner = EnhancedTestRunner()
        
        # 检测函数名
        func_name = runner.detect_test_function("test/simple.py")
        print(f"   检测到的函数名: {func_name}")
        
        # 运行测试
        result = runner.run_test("test/simple.py", test_function=func_name)
        print(f"   成功: {result['success']}")
        print(f"   测试通过: {result['test_passed']}")
        print(f"   时间: {result['execution_time']:.2f}s")
        print(f"   路径: {result['paths_explored']}")
        
        if result['success']:
            print("\n   输出摘要:")
            lines = result['output'].split('\n')
            for i, line in enumerate(lines[:10]):
                print(f"     {line}")
            if len(lines) > 10:
                print("     ...")
        else:
            print(f"\n   错误: {result['error_output'][:100]}")
    
    print("\n" + "=" * 60)
    
    # 测试我们自己创建的简单测试
    if os.path.exists("simple_correct_test.py"):
        print("2. 测试自定义示例: simple_correct_test.py")
        runner = EnhancedTestRunner()
        
        func_name = runner.detect_test_function("simple_correct_test.py")
        print(f"   检测到的函数名: {func_name}")
        
        result = runner.run_test("simple_correct_test.py", test_function=func_name)
        print(f"   成功: {result['success']}")
        print(f"   测试通过: {result['test_passed']}")
        print(f"   时间: {result['execution_time']:.2f}s")
        print(f"   路径: {result['paths_explored']}")
    
    print("\n" + "=" * 60)
    
    # 测试生成的适配器
    if os.path.exists("generated_adapter_example.py"):
        print("3. 测试生成的适配器: generated_adapter_example.py")
        runner = EnhancedTestRunner()
        
        func_name = runner.detect_test_function("generated_adapter_example.py")
        print(f"   检测到的函数名: {func_name}")
        
        result = runner.run_test("generated_adapter_example.py", test_function=func_name)
        print(f"   成功: {result['success']}")
        print(f"   测试通过: {result['test_passed']}")
        print(f"   时间: {result['execution_time']:.2f}s")
        print(f"   路径: {result['paths_explored']}")
    
    print("\n" + "=" * 60)


def create_and_test_simple_adapter():
    """创建并测试简单适配器"""
    print("创建并测试简单适配器")
    print("=" * 60)
    
    # 创建简单适配器
    simple_adapter = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from symbolic.args import symbolic

@symbolic(x=10)
def simple_test_function(x):
    """简单测试函数"""
    if x > 5:
        return "greater"
    else:
        return "less_or_equal"

def expected_result():
    """期望结果"""
    return ["greater", "less_or_equal"]

def main():
    """手动测试"""
    print("简单适配器手动测试")
    test_values = [3, 7]
    for val in test_values:
        result = simple_test_function(val)
        print(f"x={val}: {result}")

if __name__ == "__main__":
    main()
'''
    
    # 保存文件
    test_file = "simple_test_adapter.py"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(simple_adapter)
    
    print(f"创建适配器文件: {test_file}")
    
    # 运行测试
    runner = EnhancedTestRunner()
    
    print("\n1. 使用增强测试运行器:")
    result = runner.run_test(test_file)
    print(f"   成功: {result['success']}")
    print(f"   测试通过: {result['test_passed']}")
    print(f"   时间: {result['execution_time']:.2f}s")
    print(f"   路径: {result['paths_explored']}")
    
    print("\n2. 直接运行PyExZ3命令:")
    direct_result = runner.run_direct_pyexz3_test(test_file)
    print(f"   成功: {direct_result['success']}")
    print(f"   返回码: {direct_result['return_code']}")
    print(f"   时间: {direct_result['execution_time']:.2f}s")
    
    # 清理文件
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n清理文件: {test_file}")
    
    print("\n" + "=" * 60)


def verify_pyexz3_functionality():
    """验证PyExZ3核心功能"""
    print("验证PyExZ3核心功能")
    print("=" * 60)
    
    # 检查文件是否存在
    required_files = ["pyexz3.py", "symbolic/", "test/"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"缺少必要文件: {missing_files}")
        return
    
    print("基本文件检查通过")
    
    # 运行简单命令测试
    print("\n运行PyExZ3版本检查:")
    try:
        result = subprocess.run(
            ["python", "pyexz3.py", "--version"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        print(f"输出: {result.stdout.strip()}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "=" * 60)
    
    # 创建最简单的测试
    minimal_test = '''#!/usr/bin/env python
from symbolic.args import symbolic

@symbolic(x=5)
def minimal_test(x):
    if x > 2:
        return 1
    else:
        return 0

def expected_result():
    return [0, 1]
'''
    
    minimal_file = "minimal_test.py"
    with open(minimal_file, 'w', encoding='utf-8') as f:
        f.write(minimal_test)
    
    print(f"创建最小测试文件: {minimal_file}")
    
    # 直接运行测试
    print("\n运行最小测试:")
    cmd = f'python pyexz3.py --z3 --max-iters=3 --start=minimal_test {minimal_file}'
    print(f"命令: {cmd}")
    print("-" * 40)
    
    try:
        return_code = os.system(cmd)
        print(f"返回码: {return_code}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 清理
    if os.path.exists(minimal_file):
        os.remove(minimal_file)
        print(f"\n清理文件: {minimal_file}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("增强版符号执行测试运行器")
    print("=" * 60)
    
    # 验证核心功能
    verify_pyexz3_functionality()
    
    # 测试基本PyExZ3功能
    test_basic_pyexz3()
    
    # 创建并测试简单适配器
    create_and_test_simple_adapter()
    
    print("\n测试完成！")
    print("=" * 60)