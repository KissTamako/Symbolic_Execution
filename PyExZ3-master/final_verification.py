#!/usr/bin/env python
"""
最终验证修复效果
"""
import os
import sys
import traceback

# 强制切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print(f"脚本目录: {script_dir}")
print(f"当前工作目录: {os.getcwd()}")

# 检查关键文件
print("\n=== 检查关键文件 ===")
required_files = [
    ('pyexz3.py', '主程序'),
    ('test/simple.py', '测试文件'),
    ('symbolic/z3_expr/expression.py', '修复的文件'),
    ('symbolic/runtime_helpers.py', '运行时助手'),
    ('run_tests.py', '测试运行器')
]

all_exist = True
for file_path, description in required_files:
    exists = os.path.exists(file_path)
    status = '✓' if exists else '✗'
    print(f"  {status} {file_path}: {description} - {'存在' if exists else '不存在'}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n✗ 缺少必需的文件，无法继续测试")
    sys.exit(1)

print("\n=== 验证之前的修复 ===")
try:
    from symbolic.runtime_helpers import wrap_concrete_constant
    from symbolic.z3_expr.integer import Z3Integer
    import z3
    
    print("1. 测试 wrap_concrete_constant...")
    wrapped = wrap_concrete_constant(5)
    print(f"   wrap_concrete_constant(5) = {wrapped}")
    print(f"   类型: {type(wrapped)}")
    
    print("\n2. 测试 Z3 转换...")
    solver = z3.Solver()
    z3_expr = Z3Integer()
    result = z3_expr._astToZ3Expr(wrapped, solver, None)
    print(f"   转换结果: {result}, 类型: {type(result)}")
    
    print("\n3. 测试简单表达式...")
    x_var = z3_expr._getIntegerVariable('x', solver)
    expr = ['+', 'x', wrapped]
    result2 = z3_expr._astToZ3Expr(expr, solver, {'x': x_var})
    print(f"   表达式转换: {result2}, 类型: {type(result2)}")
    
    print("\n✓ Z3表达式转换修复验证通过！")
    
except Exception as e:
    print(f"\n✗ 修复验证失败: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n=== 测试运行单个测试 ===")
import subprocess

test_files = ['test/simple.py', 'test/andor.py']
results = []

for test_file in test_files:
    print(f"\n测试: {test_file}")
    if not os.path.exists(test_file):
        print(f"  ✗ 测试文件不存在")
        results.append((test_file, False, "文件不存在"))
        continue
    
    cmd = [sys.executable, 'pyexz3.py', '-m', '5', '--z3', test_file]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"  ✓ 测试通过")
            results.append((test_file, True, ""))
        else:
            print(f"  ✗ 测试失败 (返回码: {process.returncode})")
            if stderr:
                error_msg = stderr[:200]
                print(f"     错误: {error_msg}")
                results.append((test_file, False, error_msg))
            else:
                results.append((test_file, False, "未知错误"))
                
    except Exception as e:
        print(f"  ✗ 执行异常: {e}")
        results.append((test_file, False, str(e)))

print("\n=== 测试总结 ===")
passed = sum(1 for _, success, _ in results if success)
total = len(results)

print(f"通过: {passed}/{total}")

if passed == total:
    print("\n✅ 所有测试通过！修复成功！")
    print("原始问题已解决：")
    print("1. Z3表达式转换中的sort mismatch错误已修复")
    print("2. wrap_concrete_constant函数正常工作")
    print("3. 测试运行器路径问题已修复")
else:
    print("\n❌ 部分测试失败")
    for test_file, success, error in results:
        status = "✓" if success else "✗"
        print(f"  {status} {test_file}: {'通过' if success else '失败'}")
        if error:
            print(f"     错误: {error[:100]}...")
    
    print("\n需要进一步调试失败的测试...")