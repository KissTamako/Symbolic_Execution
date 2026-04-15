import sys
import os
import time

# 确保能导入pyexz3模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

# 测试用例列表
test_cases = [
    "test/simple.py",
    "test/binary_search.py"
]

# 执行模式列表
execution_modes = ["symbolic", "concolic", "concrete"]

# 路径探索策略列表
path_strategies = ["bfs", "dfs", "smart"]

# 运行测试用例的函数
def run_test(test_case, execution_mode, path_strategy):
    """运行测试用例并返回结果"""
    print(f"\nRunning test: {test_case}")
    print(f"Execution mode: {execution_mode}")
    print(f"Path strategy: {path_strategy}")
    
    start_time = time.time()
    
    # 构建命令
    command = f"python pyexz3.py --mode function --execution-mode {execution_mode} --path-selection-strategy {path_strategy} {test_case}"
    
    # 执行命令
    import subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Execution time: {execution_time:.4f} seconds")
    print(f"Return code: {result.returncode}")
    print(f"Output:\n{result.stdout}")
    
    if result.stderr:
        print(f"Error:\n{result.stderr}")
    
    return {
        "test_case": test_case,
        "execution_mode": execution_mode,
        "path_strategy": path_strategy,
        "execution_time": execution_time,
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr
    }

# 主函数
def main():
    """运行所有测试用例，使用不同的执行模式和路径探索策略"""
    print("Testing optimization effects...")
    print("=" * 80)
    
    results = []
    
    # 运行每个测试用例，使用不同的执行模式和路径探索策略
    for test_case in test_cases:
        for execution_mode in execution_modes:
            # 对于concrete模式，只使用默认的路径策略
            if execution_mode == "concrete":
                result = run_test(test_case, execution_mode, "bfs")
                results.append(result)
            else:
                for path_strategy in path_strategies:
                    result = run_test(test_case, execution_mode, path_strategy)
                    results.append(result)
    
    print("=" * 80)
    print("Test summary:")
    
    # 分析结果
    for test_case in test_cases:
        print(f"\nTest case: {test_case}")
        
        # 按执行模式分组
        mode_results = {}
        for result in results:
            if result["test_case"] == test_case:
                mode = result["execution_mode"]
                if mode not in mode_results:
                    mode_results[mode] = []
                mode_results[mode].append(result)
        
        # 打印每个执行模式的结果
        for mode, mode_result_list in mode_results.items():
            print(f"  Execution mode: {mode}")
            
            # 计算平均执行时间
            total_time = sum([r["execution_time"] for r in mode_result_list])
            avg_time = total_time / len(mode_result_list)
            print(f"    Average execution time: {avg_time:.4f} seconds")
            
            # 打印每个路径策略的结果
            if mode != "concrete":
                for path_strategy in path_strategies:
                    strategy_results = [r for r in mode_result_list if r["path_strategy"] == path_strategy]
                    if strategy_results:
                        strategy_time = strategy_results[0]["execution_time"]
                        print(f"    Path strategy: {path_strategy}, Execution time: {strategy_time:.4f} seconds")

if __name__ == "__main__":
    main()
