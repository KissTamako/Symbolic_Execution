#!/usr/bin/env python
import os
import sys
import subprocess
import traceback

# 确保在正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前目录: {os.getcwd()}")

# 测试单个文件
test_file = "test/simple.py"
print(f"测试文件: {test_file}")

# 方法1: 直接调用pyexz3.py
cmd = [sys.executable, "pyexz3.py", "-m", "5", "--z3", test_file]
print(f"执行命令: {' '.join(cmd)}")

try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    print(f"返回码: {process.returncode}")
    
    if process.returncode == 0:
        print("✓ 测试通过!")
        if stdout:
            lines = stdout.strip().split('\n')
            for i, line in enumerate(lines[:15]):  # 显示前15行
                print(f"  {line}")
            if len(lines) > 15:
                print(f"  ... (总共{len(lines)}行)")
    else:
        print("✗ 测试失败!")
        if stdout:
            print(f"标准输出 (前500字符):")
            print(stdout[:500])
        if stderr:
            print(f"错误输出 (前500字符):")
            print(stderr[:500])
            
except Exception as e:
    print(f"执行异常: {type(e).__name__}: {e}")
    traceback.print_exc()

print("\n" + "="*60 + "\n")

# 测试 andor.py
test_file2 = "test/andor.py"
print(f"测试文件: {test_file2}")
cmd2 = [sys.executable, "pyexz3.py", "-m", "5", "--z3", test_file2]
print(f"执行命令: {' '.join(cmd2)}")

try:
    process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout2, stderr2 = process2.communicate()
    
    print(f"返回码: {process2.returncode}")
    
    if process2.returncode == 0:
        print("✓ 测试通过!")
        if stdout2:
            lines = stdout2.strip().split('\n')
            for i, line in enumerate(lines[:10]):
                print(f"  {line}")
    else:
        print("✗ 测试失败!")
        if stderr2:
            print(f"错误输出 (前500字符):")
            print(stderr2[:500])
            
except Exception as e:
    print(f"执行异常: {type(e).__name__}: {e}")