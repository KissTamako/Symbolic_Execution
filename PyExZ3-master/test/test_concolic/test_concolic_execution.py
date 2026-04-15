import sys
import os

# 确保能导入symbolic模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import traceback
from symbolic.explore import ExplorationEngine
from symbolic.invocation import FunctionInvocation
from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types.symbolic_str import SymbolicStr

# 测试函数
def test_function(x, y):
    """测试函数，用于concolic执行测试"""
    if x > 0:
        if y > 0:
            return "Both positive"
        else:
            return "x positive, y non-positive"
    else:
        if y > 0:
            return "x non-positive, y positive"
        else:
            return "Both non-positive"

# 测试concolic执行
def test_concolic_execution():
    """测试concolic执行机制"""
    print("Testing concolic execution...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，使用concolic执行模式
        engine = ExplorationEngine(
            invocation,
            execution_mode="concolic",
            concolic_iterations=5,
            concrete_value_strategy="random"
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=10)
        
        print(f"Generated inputs: {generated_inputs}")
        print(f"Return values: {return_values}")
        print(f"Path length: {len(path.get_current_path())}")
        
        # 验证结果
        assert len(generated_inputs) > 0, "No inputs generated"
        assert len(return_values) > 0, "No return values"
        
        print("Concolic execution test passed!")
        return True
        
    except Exception as e:
        print(f"Error in concolic execution test: {e}")
        traceback.print_exc()
        return False

# 测试具体执行
def test_concrete_execution():
    """测试具体执行机制"""
    print("\nTesting concrete execution...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，使用concrete执行模式
        engine = ExplorationEngine(
            invocation,
            execution_mode="concrete"
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=1)
        
        print(f"Generated inputs: {generated_inputs}")
        print(f"Return values: {return_values}")
        
        # 验证结果
        assert len(generated_inputs) == 1, "Should generate exactly one input for concrete execution"
        assert len(return_values) == 1, "Should have exactly one return value for concrete execution"
        
        print("Concrete execution test passed!")
        return True
        
    except Exception as e:
        print(f"Error in concrete execution test: {e}")
        traceback.print_exc()
        return False

# 测试符号执行（作为对比）
def test_symbolic_execution():
    """测试符号执行机制（作为对比）"""
    print("\nTesting symbolic execution...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，使用symbolic执行模式
        engine = ExplorationEngine(
            invocation,
            execution_mode="symbolic"
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=10)
        
        print(f"Generated inputs: {generated_inputs}")
        print(f"Return values: {return_values}")
        print(f"Path length: {len(path.get_current_path())}")
        
        # 验证结果
        assert len(generated_inputs) > 0, "No inputs generated"
        assert len(return_values) > 0, "No return values"
        
        print("Symbolic execution test passed!")
        return True
        
    except Exception as e:
        print(f"Error in symbolic execution test: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running concolic execution tests...")
    print("=" * 60)
    
    test_results = []
    test_results.append(test_concolic_execution())
    test_results.append(test_concrete_execution())
    test_results.append(test_symbolic_execution())
    
    print("=" * 60)
    print("Test summary:")
    print(f"Total tests: {len(test_results)}")
    print(f"Passed tests: {sum(test_results)}")
    print(f"Failed tests: {len(test_results) - sum(test_results)}")
    
    if all(test_results):
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)
