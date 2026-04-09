#!/usr/bin/env python
"""
评估当前测试状态，了解失败模式
"""
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("=== 测试状态评估 ===")
print(f"当前目录: {os.getcwd()}")

# 关键测试文件列表
key_tests = [
    'test/simple.py',           # 已知通过，作为基线
    'test/len_test.py',         # 已知有问题
    'test/bignum.py',           # 文档提到的失败测试
    'test/decorator.py',        # 文档提到的失败测试
    'test/abs_test.py',         # 数学函数测试
    'test/andor.py',            # 逻辑操作测试
    'test/whileloop.py',        # 循环测试
]

# 逐个测试运行，收集详细错误信息
results = {}
for test_file in key_tests:
    if not os.path.exists(test_file):
        print(f"[跳过] {test_file} 不存在")
        results[test_file] = {'exists': False}
        continue
    
    print(f"\n--- 测试 {test_file} ---")
    
    # 使用pyexz3.py直接运行
    cmd = [sys.executable, 'pyexz3.py', '--z3', '-m', '25', test_file]
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        passed = result.returncode == 0
        results[test_file] = {
            'exists': True,
            'passed': passed,
            'returncode': result.returncode,
            'stdout_lines': len(result.stdout.splitlines()),
            'stderr_lines': len(result.stderr.splitlines())
        }
        
        if passed:
            print(f"结果: ✓ 通过")
        else:
            print(f"结果: ✗ 失败 (返回码: {result.returncode})")
            
            # 分析错误类型
            error_output = result.stderr if result.stderr else result.stdout
            if not error_output:
                print("错误输出: (空)")
            else:
                # 提取关键错误信息
                lines = error_output.split('\n')
                error_summary = []
                for line in lines[:10]:  # 只看前10行
                    if any(keyword in line.lower() for keyword in ['error', 'exception', 'traceback', 'failed']):
                        error_summary.append(line[:200])
                
                if error_summary:
                    print("错误摘要:")
                    for err in error_summary[:3]:
                        print(f"  {err}")
                
    except Exception as e:
        print(f"执行异常: {e}")
        results[test_file] = {'exists': True, 'error': str(e)}

# 分析总结
print("\n=== 测试状态总结 ===")
total_tests = len(key_tests)
existing_tests = sum(1 for r in results.values() if r.get('exists', False))
passed_tests = sum(1 for r in results.values() if r.get('passed', False))

print(f"总关键测试: {total_tests}")
print(f"存在测试文件: {existing_tests}")
print(f"通过测试: {passed_tests}")

# 失败模式分析
print("\n=== 失败模式分析 ===")
failure_modes = {
    'import_error': 0,
    'symbolic_error': 0,
    'type_error': 0,
    'other': 0
}

for test_file, result in results.items():
    if result.get('exists') and not result.get('passed'):
        # 检查stderr中是否有特定错误模式
        if 'stderr' in result:
            stderr = result.get('stderr', '')
            if 'ImportError' in stderr or 'ModuleNotFoundError' in stderr:
                failure_modes['import_error'] += 1
                print(f"{test_file}: 导入错误")
            elif 'Symbolic' in stderr or 'symbolic' in stderr:
                failure_modes['symbolic_error'] += 1
                print(f"{test_file}: 符号执行错误")
            elif 'TypeError' in stderr or 'AttributeError' in stderr:
                failure_modes['type_error'] += 1
                print(f"{test_file}: 类型错误")
            else:
                failure_modes['other'] += 1
                print(f"{test_file}: 其他错误")

print(f"\n失败模式统计:")
for mode, count in failure_modes.items():
    if count > 0:
        print(f"  {mode}: {count}")

# 建议
print("\n=== 改进建议 ===")
if failure_modes['import_error'] > 0:
    print("1. 优先修复模块导入问题")
if failure_modes['symbolic_error'] > 0:
    print("2. 检查符号执行核心逻辑")
if failure_modes['type_error'] > 0:
    print("3. 修复类型转换和属性访问")

print("\n建议从修复导入问题开始，然后逐步处理符号执行和类型错误。")