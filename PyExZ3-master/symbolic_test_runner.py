#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
符号执行测试运行器
面向学生代码的增强型符号执行工具 - 测试运行模块

功能：
1. 运行符号执行测试（PyExZ3）
2. 收集和分析测试结果
3. 监控执行过程
4. 生成测试报告
"""

import subprocess
import sys
import os
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class SymbolicTestRunner:
    """符号执行测试运行器"""
    
    def __init__(self, pyexz3_path: str = "pyexz3.py"):
        """
        初始化测试运行器
        
        Args:
            pyexz3_path: PyExZ3主程序路径
        """
        self.pyexz3_path = pyexz3_path
        self.results = []
        
    def run_test(self, adapter_file: str, test_function: str = "test_student_code", 
                max_iters: int = 5, use_z3: bool = True, timeout: int = 30) -> Dict[str, Any]:
        """
        运行单个符号执行测试
        
        Args:
            adapter_file: 适配器文件路径
            test_function: 测试函数名
            max_iters: 最大迭代次数
            use_z3: 是否使用Z3求解器
            timeout: 超时时间（秒）
            
        Returns:
            测试结果字典
        """
        start_time = time.time()
        
        try:
            # 构建PyExZ3命令
            cmd = [
                "python", self.pyexz3_path,
                f"--max-iters={max_iters}",
                f"--start={test_function}"
            ]
            
            if use_z3:
                cmd.append("--z3")
            
            cmd.append(adapter_file)
            
            # 运行命令
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 分析输出
            output = process.stdout
            error_output = process.stderr
            
            # 解析结果
            test_passed = "test passed" in output
            paths_explored = self._extract_paths_count(output)
            constraints_solved = self._extract_constraints_count(output)
            
            result = {
                'success': process.returncode == 0,
                'test_passed': test_passed,
                'return_code': process.returncode,
                'execution_time': execution_time,
                'paths_explored': paths_explored,
                'constraints_solved': constraints_solved,
                'output': output,
                'error_output': error_output,
                'command': ' '.join(cmd),
                'adapter_file': adapter_file,
                'test_function': test_function
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
                'constraints_solved': 0,
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
                'constraints_solved': 0,
                'output': '',
                'error_output': f"执行异常: {e}",
                'command': '',
                'adapter_file': adapter_file,
                'test_function': test_function
            }
    
    def run_multiple_tests(self, adapter_files: List[str], test_function: str = "test_student_code",
                          max_iters: int = 5, use_z3: bool = True, timeout: int = 30) -> List[Dict[str, Any]]:
        """
        运行多个符号执行测试
        
        Args:
            adapter_files: 适配器文件路径列表
            test_function: 测试函数名
            max_iters: 最大迭代次数
            use_z3: 是否使用Z3求解器
            timeout: 超时时间（秒）
            
        Returns:
            测试结果列表
        """
        results = []
        
        for i, adapter_file in enumerate(adapter_files):
            print(f"[{i+1}/{len(adapter_files)}] 测试文件: {adapter_file}")
            
            result = self.run_test(
                adapter_file=adapter_file,
                test_function=test_function,
                max_iters=max_iters,
                use_z3=use_z3,
                timeout=timeout
            )
            
            results.append(result)
            
            # 显示简要结果
            status = "✓ 成功" if result['success'] else "✗ 失败"
            if result.get('timeout'):
                status = "⏱️ 超时"
            
            print(f"    状态: {status}, 时间: {result['execution_time']:.2f}s, 路径: {result['paths_explored']}")
            
            if not result['success'] and result['error_output']:
                print(f"    错误: {result['error_output'][:100]}...")
        
        return results
    
    def _extract_paths_count(self, output: str) -> int:
        """从输出中提取路径探索数量"""
        # 查找类似 "Explored 5 paths" 的模式
        import re
        
        # 模式1: PyExZ3标准输出
        pattern1 = r'Explored\s+(\d+)\s+paths'
        match1 = re.search(pattern1, output, re.IGNORECASE)
        if match1:
            return int(match1.group(1))
        
        # 模式2: 调试输出中的路径计数
        lines = output.split('\n')
        path_count = 0
        for line in lines:
            if 'path' in line.lower() and any(c.isdigit() for c in line):
                # 提取数字
                numbers = re.findall(r'\d+', line)
                if numbers:
                    path_count = max(path_count, int(numbers[0]))
        
        return path_count
    
    def _extract_constraints_count(self, output: str) -> int:
        """从输出中提取约束求解数量"""
        # 查找约束求解相关信息
        import re
        
        patterns = [
            r'constraints?\s*:\s*(\d+)',
            r'solved\s+(\d+)\s+constraints',
            r'约束.*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 0
    
    def generate_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成测试报告"""
        if not results:
            return {'error': '没有测试结果'}
        
        # 统计信息
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r['success'])
        failed_tests = total_tests - successful_tests
        timeout_tests = sum(1 for r in results if r.get('timeout', False))
        
        # 执行时间统计
        execution_times = [r['execution_time'] for r in results if 'execution_time' in r]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # 路径探索统计
        paths_explored = [r['paths_explored'] for r in results]
        total_paths = sum(paths_explored)
        avg_paths = total_paths / len(paths_explored) if paths_explored else 0
        
        # 成功率
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # 详细结果
        detailed_results = []
        for i, result in enumerate(results):
            detailed_results.append({
                'index': i + 1,
                'file': result.get('adapter_file', 'unknown'),
                'success': result['success'],
                'test_passed': result.get('test_passed', False),
                'execution_time': result.get('execution_time', 0),
                'paths_explored': result.get('paths_explored', 0),
                'timeout': result.get('timeout', False),
                'error': result.get('error_output', '')[:200] if not result['success'] else ''
            })
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'timeout_tests': timeout_tests,
                'success_rate': success_rate,
                'total_execution_time': sum(execution_times),
                'average_execution_time': avg_execution_time,
                'total_paths_explored': total_paths,
                'average_paths_per_test': avg_paths
            },
            'detailed_results': detailed_results,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'pyexz3_version': self._get_pyexz3_version()
        }
        
        return report
    
    def _get_pyexz3_version(self) -> str:
        """获取PyExZ3版本信息"""
        try:
            result = subprocess.run(
                ["python", self.pyexz3_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.stdout else "未知版本"
        except:
            return "未知版本"
    
    def save_report(self, report: Dict[str, Any], output_file: str):
        """保存测试报告到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"报告已保存到: {output_file}")
        except Exception as e:
            print(f"保存报告失败: {e}")
    
    def print_report(self, report: Dict[str, Any]):
        """打印测试报告"""
        print("\n" + "=" * 70)
        print("符号执行测试报告")
        print("=" * 70)
        
        summary = report['summary']
        print(f"测试时间: {report['timestamp']}")
        print(f"PyExZ3版本: {report['pyexz3_version']}")
        print()
        
        print("概要统计:")
        print(f"  总测试数: {summary['total_tests']}")
        print(f"  成功测试: {summary['successful_tests']} ({summary['success_rate']:.1f}%)")
        print(f"  失败测试: {summary['failed_tests']}")
        print(f"  超时测试: {summary['timeout_tests']}")
        print(f"  总执行时间: {summary['total_execution_time']:.2f}秒")
        print(f"  平均执行时间: {summary['average_execution_time']:.2f}秒/测试")
        print(f"  总探索路径: {summary['total_paths_explored']}")
        print(f"  平均路径数: {summary['average_paths_per_test']:.1f}路径/测试")
        print()
        
        print("详细结果:")
        print("-" * 70)
        for result in report['detailed_results']:
            status = "✓" if result['success'] else "✗"
            if result.get('timeout'):
                status = "⏱️"
            
            print(f"{status} [{result['index']:2d}] {result['file']}")
            print(f"    时间: {result['execution_time']:.2f}s, 路径: {result['paths_explored']}, "
                  f"测试通过: {'是' if result['test_passed'] else '否'}")
            
            if result['error']:
                print(f"    错误: {result['error']}")
            print()


# ========== 使用示例和测试 ==========

def run_example_tests():
    """运行示例测试"""
    
    # 创建测试运行器
    runner = SymbolicTestRunner()
    
    # 测试文件列表
    test_files = []
    
    # 1. 使用PyExZ3自带的简单测试
    if os.path.exists("test/simple.py"):
        test_files.append("test/simple.py")
        print("添加测试文件: test/simple.py")
    
    # 2. 使用我们之前创建的简单测试
    if os.path.exists("simple_correct_test.py"):
        test_files.append("simple_correct_test.py")
        print("添加测试文件: simple_correct_test.py")
    
    # 3. 使用universal_adapter_generator生成的示例适配器
    if os.path.exists("generated_adapter_example.py"):
        test_files.append("generated_adapter_example.py")
        print("添加测试文件: generated_adapter_example.py")
    
    if not test_files:
        print("错误: 没有找到测试文件")
        return
    
    print(f"\n开始运行 {len(test_files)} 个符号执行测试...")
    print("=" * 60)
    
    # 运行测试
    results = runner.run_multiple_tests(
        adapter_files=test_files,
        test_function="test_student_code",
        max_iters=5,
        use_z3=True,
        timeout=30
    )
    
    # 生成报告
    report = runner.generate_report(results)
    
    # 打印报告
    runner.print_report(report)
    
    # 保存报告
    report_file = "symbolic_execution_report.json"
    runner.save_report(report, report_file)
    
    # 额外：运行单个详细测试示例
    if test_files:
        print("\n" + "=" * 60)
        print("详细测试示例:")
        print("=" * 60)
        
        first_test = test_files[0]
        print(f"运行详细测试: {first_test}")
        
        detailed_result = runner.run_test(
            adapter_file=first_test,
            test_function="test_student_code",
            max_iters=5,
            use_z3=True,
            timeout=30
        )
        
        print(f"命令: {detailed_result['command']}")
        print(f"返回码: {detailed_result['return_code']}")
        print(f"执行时间: {detailed_result['execution_time']:.2f}秒")
        print(f"路径探索: {detailed_result['paths_explored']}")
        print(f"测试通过: {detailed_result['test_passed']}")
        
        if detailed_result['success']:
            print("\n输出片段:")
            print("-" * 40)
            lines = detailed_result['output'].split('\n')[:20]
            for line in lines:
                print(line)
            if len(detailed_result['output'].split('\n')) > 20:
                print("... (输出截断)")
        else:
            print(f"\n错误输出: {detailed_result['error_output']}")


def test_specific_adapter():
    """测试特定的适配器文件"""
    
    # 生成一个简单的适配器进行测试
    simple_code = '''
def simple_test(x):
    if x > 10:
        return 100
    elif x > 5:
        return 50
    else:
        return 0
'''
    
    # 保存测试代码
    test_file = "test_simple_adapter.py"
    
    adapter_code = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from symbolic.args import *

{simple_code}

@symbolic(x=15)
def test_student_code(x):
    """测试函数"""
    return simple_test(x)

def expected_result():
    """期望结果"""
    return [0, 50, 100]

def main():
    """主测试"""
    print("简单适配器测试")
    test_values = [3, 7, 12]
    for test_val in test_values:
        result = test_student_code(test_val)
        print(f"x={{test_val}}: {{result}}")

if __name__ == "__main__":
    main()
'''
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(adapter_code)
    
    print(f"创建测试文件: {test_file}")
    
    # 运行测试
    runner = SymbolicTestRunner()
    result = runner.run_test(
        adapter_file=test_file,
        test_function="test_student_code",
        max_iters=5,
        use_z3=True,
        timeout=30
    )
    
    print(f"\n测试结果:")
    print(f"  成功: {result['success']}")
    print(f"  测试通过: {result['test_passed']}")
    print(f"  时间: {result['execution_time']:.2f}s")
    print(f"  路径: {result['paths_explored']}")
    
    if result['success']:
        print("\n输出:")
        print("-" * 40)
        print(result['output'][:500])
        if len(result['output']) > 500:
            print("... (输出截断)")
    else:
        print(f"\n错误: {result['error_output']}")
    
    # 清理
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n清理测试文件: {test_file}")


if __name__ == "__main__":
    print("符号执行测试运行器")
    print("=" * 60)
    
    # 运行示例测试
    run_example_tests()
    
    print("\n" + "=" * 60)
    print("特定适配器测试:")
    print("=" * 60)
    
    # 运行特定适配器测试
    test_specific_adapter()