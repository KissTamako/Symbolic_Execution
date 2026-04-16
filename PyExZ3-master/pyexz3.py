# Copyright: see copyright.txt

import os
import sys
import logging
import traceback
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine

# Get the directory of the current file
try:
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
except NameError:
    # If __file__ is not defined (e.g., when executed via exec), use the current working directory
    current_dir = os.path.abspath(os.getcwd())
sys.path = [current_dir] + sys.path

def run_function_mode(filename, entry="", max_iters=0, solver="z3", 
                     enable_frontier_dedup=False, search_strategy="bfs", 
                     enable_simplify=False, enable_prefix_dedup=False, 
                     max_prefix_length=2, enable_incremental=False, 
                     dump_all_executions=False, execution_mode="symbolic", 
                     concolic_iterations=10, concrete_value_strategy="random", 
                     path_selection_strategy="bfs", enable_path_pruning=False, 
                     enable_hybrid_search=False, path_priority_weight=0.5, 
                     dump_constraints=False, dump_trace=False, dump_semantics=False, 
                     dot_graph=False):
    """Run PyExZ3 in function mode"""
    filename = os.path.abspath(filename)
    
    # Use Loader for function mode
    app = loaderFactory(filename, entry)
    if app == None:
        return False
    print ("Exploring " + app.getFile() + "." + app.getEntry())
    print ("Mode: function")
    result = None
    
    try:
        # 为每个测试创建独立的输出目录
        test_name = os.path.basename(filename)
        test_name_no_ext = os.path.splitext(test_name)[0]
        output_dir = os.path.join(current_dir, "outputs", test_name_no_ext)
        os.makedirs(output_dir, exist_ok=True)
        
        engine = ExplorationEngine(
            app.createInvocation(), 
            solver=solver, 
            output_dir=output_dir,
            enable_frontier_dedup=enable_frontier_dedup,
            search_strategy=search_strategy,
            enable_simplify=enable_simplify,
            enable_prefix_dedup=enable_prefix_dedup,
            max_prefix_length=max_prefix_length,
            enable_incremental=enable_incremental,
            dump_all_executions=dump_all_executions,
            execution_mode=execution_mode,
            concolic_iterations=concolic_iterations,
            concrete_value_strategy=concrete_value_strategy,
            path_selection_strategy=path_selection_strategy,
            enable_path_pruning=enable_path_pruning,
            enable_hybrid_search=enable_hybrid_search,
            path_priority_weight=path_priority_weight
        )
        generatedInputs, returnVals, path = engine.explore(
            max_iters,
            dump_constraints=dump_constraints,
            dump_trace=dump_trace,
            dump_semantics=dump_semantics
        )
        # check the result
        result = app.executionComplete(returnVals)

        # output DOT graph
        if dot_graph:
            file = open(filename+".dot","w")
            file.write(path.toDot())	
            file.close()

        # Handle dump options
        if dump_constraints:
            print("Dumping constraints...")
        
        if dump_trace:
            print("Dumping trace...")
        
        if dump_semantics:
            print("Dumping semantics...")
    
    except ImportError as e:
        # createInvocation can raise this
        logging.error(e)
        return False
    
    return result

def count_input_calls(filename):
    """Count the number of input() calls in a Python script"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用简单的字符串匹配来统计 input() 调用次数
        # 这样可以避免使用 ast 模块带来的复杂性
        count = 0
        import re
        # 匹配 input() 调用，包括带参数的情况
        pattern = r'\binput\s*\('
        count = len(re.findall(pattern, content))
        return count
    except Exception:
        # 如果失败，返回 0 作为默认值
        return 0

def run_script_mode(filename, max_iters=0, solver="z3", 
                   enable_frontier_dedup=False, search_strategy="bfs", 
                   enable_simplify=False, enable_prefix_dedup=False, 
                   max_prefix_length=2, enable_incremental=False, 
                   dump_all_executions=False, execution_mode="symbolic", 
                   concolic_iterations=10, concrete_value_strategy="random", 
                   path_selection_strategy="bfs", enable_path_pruning=False, 
                   enable_hybrid_search=False, path_priority_weight=0.5, 
                   dump_constraints=False, dump_trace=False, dump_semantics=False, 
                   dot_graph=False):
    """Run PyExZ3 in script mode"""
    filename = os.path.abspath(filename)
    
    # Use ScriptRunner for script mode
    from symbolic.script_runner import ScriptRunner
    script_runner = ScriptRunner(filename)
    invocation = script_runner.create_invocation()
    
    # 识别脚本中的 input() 调用次数
    input_count = count_input_calls(filename)
    if input_count == 0:
        # 如果没有 input() 调用，添加默认的 x 和 y 输入
        invocation.add_input("x", 0)
        invocation.add_input("y", 0)
    else:
        # 根据 input() 调用次数，自动添加相应数量的输入
        for i in range(input_count):
            invocation.add_input(f"input_{i}", 0)
    
    print ("Exploring script: " + os.path.basename(filename))
    print ("Mode: script")
    print (f"Found {input_count} input() call(s)")
    result = None
    
    try:
        # 为每个测试创建独立的输出目录
        test_name = os.path.basename(filename)
        test_name_no_ext = os.path.splitext(test_name)[0]
        output_dir = os.path.join(current_dir, "outputs", test_name_no_ext)
        os.makedirs(output_dir, exist_ok=True)
        
        engine = ExplorationEngine(
            invocation, 
            solver=solver, 
            output_dir=output_dir,
            enable_frontier_dedup=enable_frontier_dedup,
            search_strategy=search_strategy,
            enable_simplify=enable_simplify,
            enable_prefix_dedup=enable_prefix_dedup,
            max_prefix_length=max_prefix_length,
            enable_incremental=enable_incremental,
            dump_all_executions=dump_all_executions,
            execution_mode=execution_mode,
            concolic_iterations=concolic_iterations,
            concrete_value_strategy=concrete_value_strategy,
            path_selection_strategy=path_selection_strategy,
            enable_path_pruning=enable_path_pruning,
            enable_hybrid_search=enable_hybrid_search,
            path_priority_weight=path_priority_weight
        )
        generatedInputs, returnVals, path = engine.explore(
            max_iters,
            dump_constraints=dump_constraints,
            dump_trace=dump_trace,
            dump_semantics=dump_semantics
        )
        # For script mode, we just check if the script executed without errors
        result = True

        # output DOT graph
        if dot_graph:
            file = open(filename+".dot","w")
            file.write(path.toDot())	
            file.close()

        # Handle dump options
        if dump_constraints:
            print("Dumping constraints...")
        
        if dump_trace:
            print("Dumping trace...")
        
        if dump_semantics:
            print("Dumping semantics...")
    
    except ImportError as e:
        # createInvocation can raise this
        logging.error(e)
        return False
    
    return result

def run_file(filename, options):
    """Run PyExZ3 on a file with given options"""
    solver = "cvc" if options.cvc else "z3"
    
    if options.mode == "script":
        return run_script_mode(
            filename,
            max_iters=options.max_iters,
            solver=solver,
            enable_frontier_dedup=options.enable_frontier_dedup,
            search_strategy=options.search_strategy,
            enable_simplify=options.enable_simplify,
            enable_prefix_dedup=options.enable_prefix_dedup,
            max_prefix_length=options.max_prefix_length,
            enable_incremental=options.enable_incremental,
            dump_all_executions=options.dump_all_executions,
            execution_mode=options.execution_mode,
            concolic_iterations=options.concolic_iterations,
            concrete_value_strategy=options.concrete_value_strategy,
            path_selection_strategy=options.path_selection_strategy,
            enable_path_pruning=options.enable_path_pruning,
            enable_hybrid_search=options.enable_hybrid_search,
            path_priority_weight=options.path_priority_weight,
            dump_constraints=options.dump_constraints,
            dump_trace=options.dump_trace,
            dump_semantics=options.dump_semantics,
            dot_graph=options.dot_graph
        )
    else:
        return run_function_mode(
            filename,
            entry=options.entry,
            max_iters=options.max_iters,
            solver=solver,
            enable_frontier_dedup=options.enable_frontier_dedup,
            search_strategy=options.search_strategy,
            enable_simplify=options.enable_simplify,
            enable_prefix_dedup=options.enable_prefix_dedup,
            max_prefix_length=options.max_prefix_length,
            enable_incremental=options.enable_incremental,
            dump_all_executions=options.dump_all_executions,
            execution_mode=options.execution_mode,
            concolic_iterations=options.concolic_iterations,
            concrete_value_strategy=options.concrete_value_strategy,
            path_selection_strategy=options.path_selection_strategy,
            enable_path_pruning=options.enable_path_pruning,
            enable_hybrid_search=options.enable_hybrid_search,
            path_priority_weight=options.path_priority_weight,
            dump_constraints=options.dump_constraints,
            dump_trace=options.dump_trace,
            dump_semantics=options.dump_semantics,
            dot_graph=options.dot_graph
        )

def parse_options(args=None):
    """Parse command line options"""
    usage = "usage: %prog [options] <path to a *.py file>"
    parser = OptionParser(usage=usage)
    
    parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file", default="")
    parser.add_option("-s", "--start", dest="entry", action="store", help="Specify entry point", default="")
    parser.add_option("-g", "--graph", dest="dot_graph", action="store_true", help="Generate a DOT graph of execution tree")
    parser.add_option("-m", "--max-iters", dest="max_iters", type="int", help="Run specified number of iterations", default=0)
    parser.add_option("--cvc", dest="cvc", action="store_true", help="Use the CVC SMT solver instead of Z3", default=False)
    parser.add_option("--z3", dest="cvc", action="store_false", help="Use the Z3 SMT solver")
    parser.add_option("--mode", dest="mode", action="store", help="Execution mode: function|script", default="function")
    parser.add_option("--dump-constraints", dest="dump_constraints", action="store_true", help="Dump constraints to files", default=False)
    parser.add_option("--dump-trace", dest="dump_trace", action="store_true", help="Dump execution trace to file", default=False)
    parser.add_option("--dump-semantics", dest="dump_semantics", action="store_true", help="Dump semantic information to file", default=False)
    
    parser.add_option("--enable-unsat-cache", dest="enable_unsat_cache", action="store_true", help="Enable UNSAT cache optimization", default=False)
    parser.add_option("--enable-frontier-dedup", dest="enable_frontier_dedup", action="store_true", help="Enable frontier constraint deduplication", default=False)
    parser.add_option("--search-strategy", dest="search_strategy", action="store", help="Search strategy: bfs|dfs", default="bfs")
    parser.add_option("--enable-simplify", dest="enable_simplify", action="store_true", help="Enable Z3 expression simplification", default=False)
    parser.add_option("--enable-prefix-dedup", dest="enable_prefix_dedup", action="store_true", help="Enable prefix deduplication (simplified)", default=False)
    parser.add_option("--max-prefix-length", dest="max_prefix_length", type="int", help="Max path length for prefix deduplication", default=2)
    parser.add_option("--enable-incremental", dest="enable_incremental", action="store_true", help="Enable incremental solving", default=False)
    parser.add_option("--dump-all-executions", dest="dump_all_executions", action="store_true", help="Dump detailed information for every execution", default=False)
    
    # Execution mode option
    parser.add_option("--execution-mode", dest="execution_mode", action="store", help="Execution mode: symbolic|concolic|concrete", default="symbolic")
    # Concolic execution parameters
    parser.add_option("--concolic-iterations", dest="concolic_iterations", type="int", help="Number of concolic execution iterations", default=10)
    parser.add_option("--concrete-value-strategy", dest="concrete_value_strategy", action="store", help="Concrete value generation strategy: random|guided|hybrid", default="random")
    
    # Path exploration strategy options
    parser.add_option("--path-selection-strategy", dest="path_selection_strategy", action="store", help="Path selection strategy: bfs|dfs|smart", default="bfs")
    parser.add_option("--enable-path-pruning", dest="enable_path_pruning", action="store_true", help="Enable path pruning", default=False)
    parser.add_option("--enable-hybrid-search", dest="enable_hybrid_search", action="store_true", help="Enable hybrid search strategy", default=False)
    parser.add_option("--path-priority-weight", dest="path_priority_weight", type="float", help="Weight for path priority calculation", default=0.5)
    
    (options, args) = parser.parse_args(args)
    return options, args

def main(args=None):
    """Main function for pyexz3"""
    print("PyExZ3 (Python Exploration with Z3)")
    
    options, args = parse_options(args)
    
    if not (options.logfile == ""):
        logging.basicConfig(filename=options.logfile,level=logging.DEBUG)
    
    if len(args) == 0 or not os.path.exists(args[0]):
        print("Missing app to execute")
        return 1
    
    result = run_file(args[0], options)
    
    if result == True:
        return 0
    elif result == None:
        # 没有 expected_result 的测试，跳过结果检查，当作成功（因为代码至少能执行）
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
