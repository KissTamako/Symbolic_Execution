#!/usr/bin/env python
"""
最小化测试andor.py
"""
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

# 直接测试符号执行
print("=== 测试andor.py符号执行 ===")

try:
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    
    # 加载应用
    app = loaderFactory('test/andor.py', 'andor', use_ast_transform=True)
    if not app:
        print("无法加载应用")
        sys.exit(1)
    
    print(f"加载: {app.getFile()}.{app.getEntry()}")
    
    # 创建调用
    inv = app.createInvocation()
    if not inv:
        print("无法创建调用")
        sys.exit(1)
    
    # 创建引擎
    engine = ExplorationEngine(inv, solver='z3')
    
    # 探索
    print("开始探索...")
    generatedInputs, returnVals, path = engine.explore(10)
    
    print(f"生成的输入数量: {len(generatedInputs)}")
    print(f"返回值数量: {len(returnVals)}")
    
    # 显示结果
    for i, (inputs, retval) in enumerate(zip(generatedInputs, returnVals)):
        print(f"路径{i}: 输入={inputs}, 返回值={retval}")
    
    # 检查是否找到了所有预期路径
    # andor有3个路径: (True,True)->1, (True,False)->1, (False,False)->2
    # (False,True) 实际上也是返回1，因为x or y为True
    # 所以实际上只有2个不同的返回值：1和2
    
    found_returns = set(returnVals)
    print(f"找到的返回值集合: {found_returns}")
    
    # 检查app.executionComplete
    result = app.executionComplete(returnVals)
    print(f"app.executionComplete(returnVals) = {result}")
    
    # 检查是否找到了所有预期路径
    if hasattr(app, 'expected_result'):
        expected = app.expected_result()
        print(f"预期结果: {expected}")
    
    # 导入andor模块获取预期结果
    import importlib.util
    spec = importlib.util.spec_from_file_location("andor", "test/andor.py")
    andor_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(andor_module)
    
    expected = andor_module.expected_result()
    print(f"从模块获取的预期结果: {expected}")
    
    # 检查是否找到了所有预期返回值
    # expected_result返回[1,1,2]，但可能有重复
    expected_set = set(expected)
    print(f"预期返回值集合: {expected_set}")
    
    if found_returns == expected_set:
        print("✓ 找到了所有预期返回值")
        sys.exit(0)
    else:
        print(f"✗ 未找到所有预期返回值: 找到{found_returns}, 预期{expected_set}")
        
        # 检查哪些缺少
        missing = expected_set - found_returns
        if missing:
            print(f"缺少的返回值: {missing}")
        
        sys.exit(1)
        
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)