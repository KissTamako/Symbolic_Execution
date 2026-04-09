#!/usr/bin/env python
import os
import sys
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

print("=== 调试Z3表达式转换 ===")

try:
    # 导入模块
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    from symbolic.z3_expr.expression import Z3Expression
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    
    print("1. 测试SymbolicInteger创建...")
    # 创建一个SymbolicInteger对象
    si = SymbolicInteger("const", 5, None)
    print(f"   SymbolicInteger创建成功: {si}, 类型: {type(si)}, 值: {si.getConcrValue()}")
    print(f"   isinstance(si, int): {isinstance(si, int)}")
    print(f"   isinstance(si, SymbolicInteger): {isinstance(si, SymbolicInteger)}")
    
    print("\n2. 测试wrap_concrete_constant...")
    from symbolic.runtime_helpers import wrap_concrete_constant
    wrapped = wrap_concrete_constant(5)
    print(f"   wrap_concrete_constant(5) = {wrapped}, 类型: {type(wrapped)}")
    print(f"   wrapped.getConcrValue() = {wrapped.getConcrValue()}")
    
    print("\n3. 测试Z3表达式转换...")
    # 创建Z3表达式转换器
    z3_expr = Z3Expression()
    
    # 尝试创建一个简单的Z3求解器
    import z3
    solver = z3.Solver()
    print(f"   Z3求解器创建成功: {solver}")
    
    # 尝试转换一个简单的表达式
    print("\n4. 测试简单表达式转换...")
    try:
        # 创建一个简单的AST表达式: (add, 'const_0', 1)
        # 其中'const_0'应该是wrap_concrete_constant创建的SymbolicInteger
        const_expr = ['add', 'const_0', 1]
        print(f"   尝试转换表达式: {const_expr}")
        
        # 需要模拟环境
        env = {'const_0': wrapped}
        
        # 尝试转换
        result = z3_expr._astToZ3Expr(const_expr, solver, env)
        print(f"   转换成功: {result}, 类型: {type(result)}")
    except Exception as e:
        print(f"   转换失败: {type(e).__name__}: {e}")
        traceback.print_exc()
        
    print("\n5. 测试实际符号执行...")
    # 加载简单测试
    app = loaderFactory('test/simple.py', 'simple', use_ast_transform=True)
    if app is None:
        print("   无法加载应用")
        sys.exit(1)
    
    print(f"   加载成功: {app.getFile()}.{app.getEntry()}")
    inv = app.createInvocation()
    engine = ExplorationEngine(inv, solver='z3')
    
    print("   开始探索...")
    try:
        generatedInputs, returnVals, path = engine.explore(2)
        print(f"   探索成功！输入: {generatedInputs}, 返回值: {returnVals}")
    except Exception as e:
        print(f"   探索失败: {type(e).__name__}: {e}")
        
        # 分析错误
        print("\n=== 详细错误分析 ===")
        tb_str = traceback.format_exc()
        
        # 查找关键信息
        if "sort mismatch" in tb_str:
            print("   发现 sort mismatch 错误")
            
            # 检查wrap_concrete_constant创建的对象的类型
            print("\n   检查wrap_concrete_constant的类型:")
            print(f"      wrap_concrete_constant(5) = {wrap_concrete_constant(5)}")
            print(f"      type = {type(wrap_concrete_constant(5))}")
            print(f"      dir = {[attr for attr in dir(wrap_concrete_constant(5)) if not attr.startswith('_')][:10]}")
            
            # 检查Z3Expression如何处理整数常量
            print("\n   检查Z3Expression._constant方法:")
            try:
                const_result = z3_expr._constant(5, solver)
                print(f"      _constant(5, solver) = {const_result}, 类型: {type(const_result)}")
            except Exception as e2:
                print(f"      _constant调用失败: {e2}")

except Exception as e:
    print(f"调试过程中发生错误: {type(e).__name__}: {e}")
    traceback.print_exc()