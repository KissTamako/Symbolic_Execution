#!/usr/bin/env python
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前目录: {os.getcwd()}")

# 使用run_tests.py的方法测试len_test.py
cmd = [sys.executable, 'run_tests.py', 'test/len_test.py', '--z3']

print(f"执行命令: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

print(f"返回码: {result.returncode}")
print("\n=== 标准输出 ===")
print(result.stdout if result.stdout else "(空)")

print("\n=== 标准错误 ===")
if result.stderr:
    print(result.stderr[:1000])
else:
    print("(空)")

# 检查输出中是否包含"passed"或"failed"
if "passed" in result.stdout.lower():
    print("\n✓ len_test.py 通过测试")
elif "failed" in result.stdout.lower():
    print("\n✗ len_test.py 测试失败")
else:
    print("\n⚠ 无法确定测试状态")