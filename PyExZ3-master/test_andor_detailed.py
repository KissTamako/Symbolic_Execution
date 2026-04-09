#!/usr/bin/env python
import os
import sys
import subprocess
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前目录: {os.getcwd()}")

test_file = "test/andor.py"
print(f"测试文件: {test_file}")

# 模拟 run_tests.py 的调用方式
print("\n=== 模拟 run_tests.py 调用方式 ===")
with open(os.devnull, 'w') as devnull:
    cmd = [sys.executable, "pyexz3.py", "-m", "25", "--z3", test_file]
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        ret = subprocess.call(cmd, stdout=devnull, stderr=subprocess.PIPE)
        print(f"返回码: {ret}")
        
        # 捕获stderr输出
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        _, stderr_output = process.communicate()
        if stderr_output:
            print(f"错误输出:\n{stderr_output.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"执行异常: {e}")
        traceback.print_exc()

# 直接运行测试查看详细输出
print("\n=== 直接运行测试（不重定向输出）===")
cmd = [sys.executable, "pyexz3.py", "-m", "25", "--z3", test_file]
print(f"执行命令: {' '.join(cmd)}")

try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout_output, stderr_output = process.communicate()
    
    print(f"返回码: {process.returncode}")
    
    if stdout_output:
        print(f"标准输出:\n{stdout_output}")
    
    if stderr_output:
        print(f"错误输出:\n{stderr_output}")
        
except Exception as e:
    print(f"执行异常: {e}")
    traceback.print_exc()