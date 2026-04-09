#!/usr/bin/env python
"""
验证runtime_helpers.py的修改是否影响现有功能
"""
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=== 验证runtime_helpers.py修改 ===")
print(f"当前目录: {os.getcwd()}")

# 1. 验证simple.py仍然通过
print("\n--- 验证simple.py ---")
cmd = [sys.executable, 'pyexz3.py', '--z3', '-m', '25', 'test/simple.py']
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='ignore')

if result.returncode == 0:
    print("[PASS] simple.py 仍然通过")
    # 检查关键输出
    if 'simple test passed' in result.stdout:
        print("[OK] 测试输出正常")
    else:
        print("[WARN] 测试输出可能异常")
else:
    print(f"[FAIL] simple.py 失败 (返回码: {result.returncode})")
    if result.stderr:
        lines = result.stderr.split('\n')
        for line in lines[:5]:
            if line.strip():
                print(f"  错误: {line[:100]}")

# 2. 验证len_test.py的错误是否变化
print("\n--- 检查len_test.py错误 ---")
cmd = [sys.executable, 'pyexz3.py', '--z3', '-m', '25', 'test/len_test.py']
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='ignore')

print(f"返回码: {result.returncode}")
if result.stdout:
    lines = result.stdout.split('\n')
    for line in lines[-10:]:
        if line.strip():
            print(f"  输出: {line[:150]}")

# 3. 直接测试runtime_helpers.py中的函数
print("\n--- 直接测试runtime_helpers函数 ---")
try:
    import symbolic.runtime_helpers as rh
    
    # 测试unwrap函数
    # 创建SymbolicInteger测试
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    
    # 测试1: 具体的整数
    test_int = 42
    unwrapped = rh.unwrap(test_int)
    print(f"unwrap(42) = {unwrapped} (应为42)")
    
    # 测试2: SymbolicInteger
    sym_int = SymbolicInteger("test", 123, None)
    unwrapped_sym = rh.unwrap(sym_int)
    print(f"unwrap(SymbolicInteger) = {unwrapped_sym} (应为123)")
    
    # 测试3: _se_int函数
    wrapped_int = rh._se_int(456)
    print(f"_se_int(456) = {wrapped_int} (应为SymbolicInteger类型)")
    print(f"  unwrap(_se_int(456)) = {rh.unwrap(wrapped_int)}")
    
    print("[OK] runtime_helpers函数基本可用")
except Exception as e:
    print(f"[ERROR] runtime_helpers测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 验证完成 ===")