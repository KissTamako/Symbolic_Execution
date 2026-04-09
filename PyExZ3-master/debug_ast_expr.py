#!/usr/bin/env python
import os
import sys
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

print("=== 调试AST表达式结构 ===")

try:
    # 导入模块
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    from symbolic.symbolic_types.symbolic_type import SymbolicType
    
    print("1. 加载测试文件...")
    app = loaderFactory('test/simple.py', 'simple', use_ast_transform=True)
    if app is None:
        print("   无法加载应用")
        sys.exit(1)
    
    print(f"   加载成功: {app.getFile()}.{app.getEntry()}")
    
    print("\n2. 创建调用和引擎...")
    inv = app.createInvocation()
    engine = ExplorationEngine(inv, solver='z3')
    
    print("\n3. 获取路径条件...")
    # 手动执行一次以获取路径条件
    print("   执行第一次调用...")
    result = inv.callFunction([])
    print(f"   结果: {result}")
    
    print("\n4. 检查路径条件结构...")
    # 获取当前路径的条件
    from symbolic.path_to_constraint import PathToConstraint
    path_to_constraint = PathToConstraint()
    
    # 获取引擎中的约束
    print("   引擎中的约束:")
    if hasattr(engine, 'solver'):
        solver = engine.solver
        print(f"   求解器类型: {type(solver)}")
        
        # 检查求解器中的约束
        if hasattr(solver, 'asserts'):
            print(f"   断言数量: {len(solver.asserts) if solver.asserts else 0}")
            if solver.asserts:
                print(f"   第一个断言: {solver.asserts[0]}")
                print(f"   类型: {type(solver.asserts[0])}")
                
        if hasattr(solver, 'query'):
            print(f"   查询: {solver.query}")
            print(f"   查询类型: {type(solver.query)}")
            
            # 检查查询的symtype属性
            if hasattr(solver.query, 'symtype'):
                print(f"   查询的symtype: {solver.query.symtype}")
                print(f"   查询的symtype类型: {type(solver.query.symtype)}")
                
                # 如果是列表，显示结构
                if isinstance(solver.query.symtype, list):
                    print(f"   symtype列表结构: {solver.query.symtype}")
                    print(f"   第一个元素: {solver.query.symtype[0] if solver.query.symtype else '空'}")
                    print(f"   第二个元素: {solver.query.symtype[1] if len(solver.query.symtype) > 1 else '无'}")
                    print(f"   第三个元素: {solver.query.symtype[2] if len(solver.query.symtype) > 2 else '无'}")
    
    print("\n5. 测试直接Z3表达式转换...")
    from symbolic.z3_expr.expression import Z3Expression
    from symbolic.predicate import Predicate
    import z3
    
    # 创建一个简单的谓词
    print("   创建简单谓词: x + 1 > 10")
    
    # 首先需要了解Predicate的结构
    print("\n   检查Predicate类...")
    pred = Predicate()
    print(f"   Predicate类: {Predicate}")
    print(f"   Predicate属性: {[attr for attr in dir(Predicate) if not attr.startswith('_')]}")
    
    # 尝试创建一个简单的AST表达式
    print("\n   创建AST表达式测试...")
    # AST表达式可能是: ['>', ['+', 'x', 1], 10]
    # 或者: ['>', ['+', 'x', wrap_concrete_constant(1)], wrap_concrete_constant(10)]
    
    # 检查wrap_concrete_constant的实际输出
    from symbolic.runtime_helpers import wrap_concrete_constant
    wrapped_1 = wrap_concrete_constant(1)
    wrapped_10 = wrap_concrete_constant(10)
    
    print(f"   wrap_concrete_constant(1): {wrapped_1}, 类型: {type(wrapped_1)}")
    print(f"   wrap_concrete_constant(10): {wrapped_10}, 类型: {type(wrapped_10)}")
    
    # 检查wrapped对象是否有name属性
    print(f"   wrapped_1.name: {wrapped_1.name if hasattr(wrapped_1, 'name') else '无name属性'}")
    print(f"   wrapped_10.name: {wrapped_10.name if hasattr(wrapped_10, 'name') else '无name属性'}")
    
    # 检查是否是SymbolicType
    print(f"   isinstance(wrapped_1, SymbolicType): {isinstance(wrapped_1, SymbolicType)}")
    
except Exception as e:
    print(f"调试过程中发生错误: {type(e).__name__}: {e}")
    traceback.print_exc()