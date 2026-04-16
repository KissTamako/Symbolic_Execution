import os
import subprocess
import sys
import time


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

test_cases = [
    "test/simple.py",
    "test/binary_search.py",
]

execution_modes = ["symbolic", "concolic", "concrete"]
path_strategies = ["bfs", "dfs", "smart"]


def run_test(test_case, execution_mode, path_strategy):
    print(f"\nRunning test: {test_case}")
    print(f"Execution mode: {execution_mode}")
    print(f"Path strategy: {path_strategy}")

    start_time = time.time()
    command = [
        sys.executable,
        "pyexz3.py",
        "--mode",
        "function",
        "--execution-mode",
        execution_mode,
        "--path-selection-strategy",
        path_strategy,
        test_case,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    execution_time = time.time() - start_time

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
        "error": result.stderr,
    }


def main():
    print("Testing optimization effects...")
    print("=" * 80)

    results = []
    has_failures = False

    for test_case in test_cases:
        for execution_mode in execution_modes:
            if execution_mode == "concrete":
                result = run_test(test_case, execution_mode, "bfs")
                results.append(result)
                has_failures = has_failures or result["return_code"] != 0
            else:
                for path_strategy in path_strategies:
                    result = run_test(test_case, execution_mode, path_strategy)
                    results.append(result)
                    has_failures = has_failures or result["return_code"] != 0

    print("=" * 80)
    print("Test summary:")

    for test_case in test_cases:
        print(f"\nTest case: {test_case}")
        mode_results = {}
        for result in results:
            if result["test_case"] != test_case:
                continue
            mode_results.setdefault(result["execution_mode"], []).append(result)

        for mode, mode_result_list in mode_results.items():
            print(f"  Execution mode: {mode}")
            total_time = sum(item["execution_time"] for item in mode_result_list)
            avg_time = total_time / len(mode_result_list)
            print(f"    Average execution time: {avg_time:.4f} seconds")

            if mode != "concrete":
                for path_strategy in path_strategies:
                    strategy_results = [item for item in mode_result_list if item["path_strategy"] == path_strategy]
                    if strategy_results:
                        print(
                            f"    Path strategy: {path_strategy}, "
                            f"Execution time: {strategy_results[0]['execution_time']:.4f} seconds"
                        )

    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
