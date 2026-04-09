#!/usr/bin/env python
import os
import sys
import subprocess
import traceback

# 获取当前目录
current_dir = os.getcwd()
print(f"当前工作目录: {current_dir}")

# 检查关键文件
print("\n检查关键文件:")
files_to_check = [
    'pyexz3.py',
    'test/simple.py',
    'symbolic/explore.py',
    'run_tests.py'
]

for f in files_to_check:
    full_path = os.path.join(current_dir, f)
    exists = os.path.exists(full_path)
    print(f"  {'✓' if exists else '✗'} {f}: {'存在' if exists else '不存在'} ({full_path})")

# 测试直接运行 pyexz3.py
print("\n=== 测试直接运行 pyexz3.py ===")
test_file = "test/simple.py"
cmd = [sys.executable, "pyexz3.py", "-m", "25", "--z3", test_file]

print(f"执行命令: {' '.join(cmd)}")

try:
    # 不重定向输出，查看实际错误
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout_output, stderr_output = process.communicate()
    
    print(f"返回码: {process.returncode}")
    
    if stdout_output:
        print(f"标准输出 (前500字符):")
        print(stdout_output[:500])
        if len(stdout_output) > 500:
            print(f"... (总共 {len(stdout_output)} 字符)")
    
    if stderr_output:
        print(f"错误输出 (前500字符):")
        print(stderr_output[:500])
        if len(stderr_output) > 500:
            print(f"... (总共 {len(stderr_output)} 字符)")
        
except Exception as e:
    print(f"执行异常: {type(e).__name__}: {e}")
    traceback.print_exc()

# 测试 run_tests.py 的内部逻辑
print("\n=== 测试 run_tests.py 的内部逻辑 ===")
# 模拟 run_tests.py 的子进程调用
cmd2 = [sys.executable, "pyexz3.py", "-m", "25", "--z3", test_file]

with open(os.devnull, 'w') as devnull:
    try:
        ret = subprocess.call(cmd2, stdout=devnull, stderr=subprocess.PIPE)
        print(f"run_tests.py 风格的调用返回码: {ret}")
        
        # 捕获 stderr
        process2 = subprocess.Popen(cmd2, stderr=subprocess.PIPE)
        _, stderr_output2 = process2.communicate()
        if stderr_output2:
            print(f"run_tests.py 风格的错误输出:")
            print(stderr_output2.decode('utf-8', errors='ignore')[:500])
    except Exception as e:
        print(f"调用异常: {e}")

# 检查路径问题
print("\n=== 检查路径问题 ===")
print(f"sys.executable: {sys.executable}")
print(f"当前目录下的 pyexz3.py 绝对路径: {os.path.abspath('pyexz3.py')}")

# 测试 Python 导入
print("\n=== 测试 Python 导入 ===")
sys.path.insert(0, '.')
try:
    import pyexz3
    print("✓ 成功导入 pyexz3")
    
    # 检查 pyexz3 的内容
    if hasattr(pyexz3, 'main'):
        print("✓ pyexz3 有 main 函数")
    else:
        print("✗ pyexz3 没有 main 函数")
        
except ImportError as e:
    print(f"✗ 无法导入 pyexz3: {e}")
    # 尝试查看 pyexz3.py 内容
    try:
        with open('pyexz3.py', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            print(f"pyexz3.py 第一行: {first_line}")
    except Exception as e2:
        print(f"无法读取 pyexz3.py: {e2}")