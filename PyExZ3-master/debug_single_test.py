#!/usr/bin/env python
"""
详细调试单个测试
"""
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 测试文件
test_file = 'test/len_test.py'
print(f"调试测试: {test_file}")
print(f"当前目录: {os.getcwd()}")

if not os.path.exists(test_file):
    print(f"错误: {test_file} 不存在")
    sys.exit(1)

# 运行测试并捕获所有输出
cmd = [sys.executable, 'pyexz3.py', '--z3', '-m', '25', test_file]
print(f"执行命令: {' '.join(cmd)}")

# 设置环境变量，确保输出是英文
env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'

try:
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True, 
        timeout=30, 
        encoding='utf-8',
        errors='ignore',
        env=env
    )
    
    print(f"\n=== 返回码: {result.returncode} ===")
    
    print("\n=== 标准输出 ===")
    if result.stdout:
        # 打印完整输出
        for i, line in enumerate(result.stdout.split('\n')[:50]):
            print(f"{i+1:3}: {line}")
    else:
        print("(空)")
    
    print("\n=== 标准错误 ===")
    if result.stderr:
        # 打印完整错误
        for i, line in enumerate(result.stderr.split('\n')[:50]):
            print(f"{i+1:3}: {line}")
    else:
        print("(空)")
        
except subprocess.TimeoutExpired:
    print("超时 (30秒)")
except Exception as e:
    print(f"执行异常: {e}")

# 检查相关文件
print("\n=== 检查导入 ===")
import_path = 'symbolic/args.py'
if os.path.exists(import_path):
    print(f"{import_path} 存在")
    with open(import_path, 'r', encoding='utf-8') as f:
        first_lines = f.readlines()[:5]
        print("前5行:")
        for i, line in enumerate(first_lines):
            print(f"  {i+1}: {line.rstrip()}")
else:
    print(f"{import_path} 不存在")

print("\n=== 调试完成 ===")