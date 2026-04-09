#!/usr/bin/env python
"""
简单测试状态评估，避免编码问题
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
]

# 逐个测试运行，收集详细错误信息
for test_file in key_tests:
    if not os.path.exists(test_file):
        print(f"[跳过] {test_file} 不存在")
        continue
    
    print(f"\n--- 测试 {test_file} ---")
    
    # 使用pyexz3.py直接运行
    cmd = [sys.executable, 'pyexz3.py', '--z3', '-m', '25', test_file]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print("结果: PASSED")
            # 简单检查输出
            if result.stdout:
                lines = result.stdout.split('\n')
                print("输出摘要:")
                for line in lines[-5:]:  # 最后5行
                    if line.strip():
                        print(f"  {line[:100]}")
        else:
            print(f"结果: FAILED (返回码: {result.returncode})")
            
            # 分析错误
            error_output = result.stderr if result.stderr else result.stdout
            if error_output:
                lines = error_output.split('\n')
                print("错误信息:")
                for line in lines[:10]:  # 前10行
                    if any(keyword in line.lower() for keyword in ['error', 'exception', 'traceback']):
                        print(f"  {line[:150]}")
            else:
                print("错误输出: (空)")
                
    except subprocess.TimeoutExpired:
        print("结果: TIMEOUT (30秒)")
    except Exception as e:
        print(f"执行异常: {e}")

print("\n=== 测试完成 ===")