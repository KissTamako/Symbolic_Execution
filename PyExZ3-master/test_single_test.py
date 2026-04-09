#!/usr/bin/env python
"""
测试单个测试文件，分析失败原因
"""
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前目录: {os.getcwd()}")

# 测试单个测试文件
test_file = 'test/simple.py'
if not os.path.exists(test_file):
    print(f"错误: {test_file} 不存在")
    sys.exit(1)

print(f"测试文件: {test_file}")

# 使用run_tests.py的方式运行单个测试
pyexz3_path = os.path.abspath('pyexz3.py')
print(f"pyexz3.py路径: {pyexz3_path}")

if not os.path.exists(pyexz3_path):
    print("错误: pyexz3.py 不存在")
    sys.exit(1)

# 运行单个测试
cmd = [sys.executable, pyexz3_path, "-m", "25", "--z3", test_file]
print(f"执行命令: {' '.join(cmd)}")

# 捕获详细输出
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
print(f"返回码: {result.returncode}")

print("\n=== 标准输出 ===")
if result.stdout:
    print(result.stdout[:1000])
else:
    print("(空)")

print("\n=== 标准错误 ===")
if result.stderr:
    print(result.stderr[:1000])
else:
    print("(空)")

# 分析可能的问题
print("\n=== 问题分析 ===")
if result.returncode != 0:
    if "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
        print("问题: 模块导入失败")
        print("可能原因: loader.py无法正确加载测试模块")
    elif "SyntaxError" in result.stderr:
        print("问题: 语法错误")
        print("可能原因: 测试文件或符号执行代码有语法错误")
    elif "AttributeError" in result.stderr:
        print("问题: 属性错误")
        print("可能原因: 符号类型或方法不存在")
    else:
        print("问题: 未知错误类型")
else:
    print("测试成功!")

# 检查test/simple.py的内容
print("\n=== 检查测试文件 ===")
with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')
    print(f"测试文件行数: {len(lines)}")
    print(f"前10行:")
    for i, line in enumerate(lines[:10]):
        print(f"  {i+1}: {line}")