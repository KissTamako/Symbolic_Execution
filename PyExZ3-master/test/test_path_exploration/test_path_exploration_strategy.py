import sys
import os

# 确保能导入symbolic模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import traceback
from symbolic.explore import ExplorationEngine
from symbolic.invocation import FunctionInvocation

# 测试函数 - 有多个分支的函数
def complex_test_function(x, y, z):
    """测试函数，用于路径探索策略测试"""
    if x > 0:
        if y > 0:
            if z > 0:
                return "All positive"
            else:
                return "x,y positive, z non-positive"
        else:
            if z > 0:
                return "x positive, y non-positive, z positive"
            else:
                return "x positive, y,z non-positive"
    else:
        if y > 0:
            if z > 0:
                return "x non-positive, y,z positive"
            else:
                return "x non-positive, y positive, z non-positive"
        else:
            if z > 0:
                return "x,y non-positive, z positive"
            else:
                return "All non-positive"

# 测试BFS搜索策略
def test_bfs_strategy():
    """测试BFS搜索策略"""
    print("Testing BFS search strategy...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(complex_test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        invocation.addArgumentConstructor("z", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，使用BFS搜索策略
        engine = ExplorationEngine(
            invocation,
            path_selection_strategy="bfs"
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=10)
        
        print(f"Generated inputs: {len(generated_inputs)}")
        print(f"Return values: {set(return_values)}")
        print(f"Unique return values: {len(set(return_values))}")
        
        # 验证结果
        assert len(generated_inputs) > 0, "No inputs generated"
        assert len(return_values) > 0, "No return values"
        
        print("BFS search strategy test passed!")
        return True
        
    except Exception as e:
        print(f"Error in BFS search strategy test: {e}")
        traceback.print_exc()
        return False

# 测试DFS搜索策略
def test_dfs_strategy():
    """测试DFS搜索策略"""
    print("\nTesting DFS search strategy...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(complex_test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        invocation.addArgumentConstructor("z", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，使用DFS搜索策略
        engine = ExplorationEngine(
            invocation,
            path_selection_strategy="dfs"
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=10)
        
        print(f"Generated inputs: {len(generated_inputs)}")
        print(f"Return values: {set(return_values)}")
        print(f"Unique return values: {len(set(return_values))}")
        
        # 验证结果
        assert len(generated_inputs) > 0, "No inputs generated"
        assert len(return_values) > 0, "No return values"
        
        print("DFS search strategy test passed!")
        return True
        
    except Exception as e:
        print(f"Error in DFS search strategy test: {e}")
        traceback.print_exc()
        return False

# 测试智能搜索策略
def test_smart_strategy():
    """测试智能搜索策略"""
    print("\nTesting smart search strategy...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(complex_test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        invocation.addArgumentConstructor("z", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，使用智能搜索策略
        engine = ExplorationEngine(
            invocation,
            path_selection_strategy="smart"
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=10)
        
        print(f"Generated inputs: {len(generated_inputs)}")
        print(f"Return values: {set(return_values)}")
        print(f"Unique return values: {len(set(return_values))}")
        
        # 验证结果
        assert len(generated_inputs) > 0, "No inputs generated"
        assert len(return_values) > 0, "No return values"
        
        print("Smart search strategy test passed!")
        return True
        
    except Exception as e:
        print(f"Error in smart search strategy test: {e}")
        traceback.print_exc()
        return False

# 测试路径剪枝
def test_path_pruning():
    """测试路径剪枝功能"""
    print("\nTesting path pruning...")
    
    try:
        # 创建函数调用对象
        def reset():
            pass
        
        invocation = FunctionInvocation(complex_test_function, reset)
        # 添加参数构造器
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        invocation.addArgumentConstructor("x", 0, SymbolicInteger)
        invocation.addArgumentConstructor("y", 0, SymbolicInteger)
        invocation.addArgumentConstructor("z", 0, SymbolicInteger)
        
        # 创建ExplorationEngine，启用路径剪枝
        engine = ExplorationEngine(
            invocation,
            enable_path_pruning=True
        )
        
        # 执行探索
        generated_inputs, return_values, path = engine.explore(max_iterations=10)
        
        print(f"Generated inputs: {len(generated_inputs)}")
        print(f"Return values: {set(return_values)}")
        print(f"Unique return values: {len(set(return_values))}")
        
        # 验证结果
        assert len(generated_inputs) > 0, "No inputs generated"
        assert len(return_values) > 0, "No return values"
        
        print("Path pruning test passed!")
        return True
        
    except Exception as e:
        print(f"Error in path pruning test: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running path exploration strategy tests...")
    print("=" * 60)
    
    test_results = []
    test_results.append(test_bfs_strategy())
    test_results.append(test_dfs_strategy())
    test_results.append(test_smart_strategy())
    test_results.append(test_path_pruning())
    
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
