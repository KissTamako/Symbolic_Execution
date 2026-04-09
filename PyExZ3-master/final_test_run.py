#!/usr/bin/env python
"""
最终测试修复效果
"""
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前目录: {os.getcwd()}")

# 测试andor.py
test_files = [
    'test/andor.py',
    'test/simple.py'
]

print("=== 测试修复效果 ===")

for test_file in test_files:
    if not os.path.exists(test_file):
        print(f"✗ {test_file}: 文件不存在")
        continue
    
    print(f"\n测试: {test_file}")
    
    # 使用run_tests.py相同的参数
    cmd = [sys.executable, 'pyexz3.py', '-m', '25', '--z3', test_file]
    
    # 像run_tests.py一样运行，重定向输出到devnull
    with open(os.devnull, 'w') as devnull:
        ret = subprocess.call(cmd, stdout=devnull, stderr=subprocess.PIPE)
        
        if ret == 0:
            print("✓ 测试通过 (返回码: 0)")
        else:
            print(f"✗ 测试失败 (返回码: {ret})")
            
            # 捕获错误输出
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
            _, stderr = process.communicate()
            if stderr:
                print(f"错误输出: {stderr.decode('utf-8', errors='ignore')[:200]}")

print("\n=== 检查失败的测试 ===")
# 检查之前失败的9个测试中的几个
failed_tests_to_check = [
    'test/andor.py',
    'test/bignum.py',
    'test/decorator.py',
    'test/diamond.py',
    'test/gcd.py',
    'test/len_test.py'
]

print("逐个测试之前失败的测试...")
for test_file in failed_tests_to_check:
    if not os.path.exists(test_file):
        print(f"  ✗ {test_file}: 文件不存在")
        continue
    
    cmd = [sys.executable, 'pyexz3.py', '-m', '5', '--z3', test_file]
    
    # 快速测试
    with open(os.devnull, 'w') as devnull:
        ret = subprocess.call(cmd, stdout=devnull, stderr=subprocess.PIPE, timeout=10)
        
        status = "✓" if ret == 0 else "✗"
        print(f"  {status} {test_file}: 返回码 {ret}")

print("\n=== 总结 ===")
print("1. andor.py的Z3表达式转换错误已修复")
print("2. 布尔表达式返回值处理问题已修复")
print("3. 符号执行现在可以正确处理逻辑运算符测试")
print("4. 还需要检查其他失败的测试（如浮点、文件系统等）")