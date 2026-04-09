#!/usr/bin/env python
"""
简单测试修复是否有效
"""
import os
import sys
import traceback

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, '.')

print(f"当前工作目录: {os.getcwd()}")
print(f"脚本目录: {script_dir}")

# 检查关键文件是否存在
print("\n检查关键文件:")
files_to_check = [
    'symbolic/z3_expr/expression.py',
    'symbolic/runtime_helpers.py',
    'symbolic/symbolic_types/symbolic_int.py',
    'test/simple.py'
]

for f in files_to_check:
    exists = os.path.exists(f)
    print(f"  {'✓' if exists else '✗'} {f}: {'存在' if exists else '不存在'}")

print("\n=== 测试修复 ===")

try:
    # 1. 测试 wrap_concrete_constant
    print("1. 测试 wrap_concrete_constant...")
    from symbolic.runtime_helpers import wrap_concrete_constant
    wrapped = wrap_concrete_constant(5)
    print(f"   wrap_concrete_constant(5) = {wrapped}")
    print(f"   类型: {type(wrapped)}")
    print(f"   name属性: {wrapped.name if hasattr(wrapped, 'name') else '无'}")
    print(f"   isVariable(): {wrapped.isVariable()}")
    
    # 2. 测试 Z3 表达式转换
    print("\n2. 测试 Z3 表达式转换...")
    from symbolic.z3_expr.integer import Z3Integer
    import z3
    
    solver = z3.Solver()
    z3_expr = Z3Integer()
    
    # 测试 _constant 方法
    const_z3 = z3_expr._constant(5, solver)
    print(f"   _constant(5, solver) = {const_z3}, 类型: {type(const_z3)}")
    
    # 测试转换 wrapped 对象
    print("\n3. 测试 SymbolicInteger 转换...")
    result = z3_expr._astToZ3Expr(wrapped, solver, None)
    print(f"   _astToZ3Expr(wrapped, solver, None) = {result}, 类型: {type(result)}")
    
    # 3. 测试实际符号执行
    print("\n4. 测试实际符号执行...")
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    
    app = loaderFactory('test/simple.py', 'simple', use_ast_transform=True)
    if app is None:
        print("   无法加载应用")
    else:
        print(f"   加载成功: {app.getFile()}.{app.getEntry()}")
        inv = app.createInvocation()
        engine = ExplorationEngine(inv, solver='z3')
        
        print("   开始探索...")
        try:
            generatedInputs, returnVals, path = engine.explore(2)
            print(f"   探索成功！")
            print(f"     生成输入: {generatedInputs}")
            print(f"     返回值: {returnVals}")
            
            # 检查是否找到两个路径
            if len(generatedInputs) >= 2:
                print("   ✓ 成功找到多个路径！")
            else:
                print(f"   ⚠ 只找到 {len(generatedInputs)} 个路径")
                
        except Exception as e:
            print(f"   探索失败: {type(e).__name__}: {e}")
            print("   错误堆栈:")
            traceback.print_exc()
            
except Exception as e:
    print(f"测试过程中发生错误: {type(e).__name__}: {e}")
    traceback.print_exc()