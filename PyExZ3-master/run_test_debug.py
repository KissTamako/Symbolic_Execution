#!/usr/bin/env python
import os
import sys
import traceback

# 确保在正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前工作目录: {os.getcwd()}")

sys.path.insert(0, '.')

try:
    print("=== 测试符号执行 ===")
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    
    print("1. 加载测试文件...")
    app = loaderFactory('test/simple.py', 'simple', use_ast_transform=True)
    if app is None:
        print("   无法加载应用")
        sys.exit(1)
    print(f"   加载成功: {app.getFile()}.{app.getEntry()}")
    
    print("2. 创建调用...")
    inv = app.createInvocation()
    print("   调用创建成功")
    
    print("3. 创建引擎...")
    engine = ExplorationEngine(inv, solver='z3')
    print("   引擎创建成功")
    
    print("4. 开始探索（最大5次迭代）...")
    generatedInputs, returnVals, path = engine.explore(5)
    print(f"   探索成功！")
    print(f"     生成输入: {generatedInputs}")
    print(f"     返回值: {returnVals}")
    
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    print("=== 完整错误堆栈 ===")
    traceback.print_exc()
    
    # 打印错误位置
    import re
    tb_str = traceback.format_exc()
    
    # 查找Z3相关的错误
    if "sort mismatch" in tb_str:
        print("\n=== 找到 sort mismatch 错误 ===")
        # 提取相关行
        lines = tb_str.split('\n')
        for i, line in enumerate(lines):
            if "sort mismatch" in line or "_astToZ3Expr" in line or "wrap_concrete_constant" in line:
                print(f"行 {i}: {line}")
    
    sys.exit(1)
