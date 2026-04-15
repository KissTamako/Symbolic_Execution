import sys
import traceback

# 确保能导入symbolic模块
sys.path.insert(0, '.')

try:
    print("Testing PyExZ3 components...")
    
    # 测试导入核心模块
    print("1. Importing symbolic modules...")
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    print("✓ Core modules imported successfully")
    
    # 测试创建loader
    print("2. Creating loader...")
    loader = loaderFactory('test_minimal.py', '')
    print("✓ Loader created successfully")
    
    # 测试创建invocation
    print("3. Creating invocation...")
    invocation = loader.createInvocation()
    print("✓ Invocation created successfully")
    
    # 测试创建ExplorationEngine
    print("4. Creating ExplorationEngine...")
    engine = ExplorationEngine(invocation, solver="z3")
    print("✓ ExplorationEngine created successfully")
    
    # 测试explore方法
    print("5. Running explore...")
    result = engine.explore(max_iterations=5)
    print(f"✓ Explore completed successfully, result: {result}")
    
    print("\nAll tests passed!")
    
except Exception as e:
    print(f"\nError: {e}")
    traceback.print_exc()
