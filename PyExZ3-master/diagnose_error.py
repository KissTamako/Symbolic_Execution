#!/usr/bin/env python
import os
import sys
import traceback

print("=== 诊断测试失败问题 ===")

# 确保在PyExZ3-master目录中
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前工作目录: {os.getcwd()}")

# 检查关键文件
key_files = [
    'pyexz3.py',
    'symbolic/z3_expr/expression.py',
    'symbolic/runtime_helpers.py',
    'test/simple.py'
]

for f in key_files:
    exists = os.path.exists(f)
    print(f"{'✓' if exists else '✗'} {f}: {'存在' if exists else '不存在'}")

print("\n=== 尝试运行简单测试 ===")

try:
    # 导入需要的模块
    sys.path.insert(0, '.')
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    
    print("✓ 成功导入模块")
    
    # 加载测试
    test_file = 'test/simple.py'
    print(f"加载测试文件: {test_file}")
    app = loaderFactory(test_file, 'simple', use_ast_transform=True)
    
    if app is None:
        print("✗ 无法加载应用")
        sys.exit(1)
    
    print(f"✓ 加载成功: {app.getFile()}.{app.getEntry()}")
    
    # 创建调用
    inv = app.createInvocation()
    print("✓ 调用创建成功")
    
    # 创建引擎
    engine = ExplorationEngine(inv, solver='z3')
    print("✓ 引擎创建成功")
    
    # 尝试探索
    print("\n=== 开始探索（带详细调试）===")
    try:
        generatedInputs, returnVals, path = engine.explore(5)
        print(f"✓ 探索成功！生成输入: {generatedInputs}")
        print(f"  返回值: {returnVals}")
    except Exception as e:
        print(f"✗ 探索失败: {e}")
        print("错误堆栈:")
        traceback.print_exc()
        
        # 尝试诊断具体问题
        print("\n=== 诊断具体问题 ===")
        
        # 检查wrap_concrete_constant
        import symbolic.runtime_helpers
        print("检查wrap_concrete_constant函数...")
        
        # 尝试创建一个符号整数
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        try:
            si = SymbolicInteger(42)
            print(f"✓ SymbolicInteger创建成功: {si}")
        except Exception as e2:
            print(f"✗ SymbolicInteger创建失败: {e2}")
            
except Exception as e:
    print(f"✗ 诊断过程中发生错误: {e}")
    print("完整错误堆栈:")
    traceback.print_exc()