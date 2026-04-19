# Copyright: see copyright.txt

import ast
import logging
import os
import sys
import traceback
from optparse import OptionParser

from symbolic.explore import ExplorationEngine
from symbolic.loader import *


try:
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
except NameError:
    current_dir = os.path.abspath(os.getcwd())
sys.path = [current_dir] + sys.path


def run_function_mode(
    filename,
    entry="",
    max_iters=0,
    solver="z3",
    enable_frontier_dedup=False,
    search_strategy="bfs",
    enable_simplify=False,
    enable_prefix_dedup=False,
    max_prefix_length=2,
    enable_incremental=False,
    dump_all_executions=False,
    execution_mode="symbolic",
    concolic_iterations=10,
    concrete_value_strategy="random",
    path_selection_strategy="bfs",
    enable_path_pruning=False,
    enable_hybrid_search=False,
    path_priority_weight=0.5,
    dump_constraints=False,
    dump_trace=False,
    dump_semantics=False,
    dot_graph=False,
):
    """Run PyExZ3 in function mode."""
    filename = os.path.abspath(filename)

    app = loaderFactory(filename, entry)
    if app is None:
        return False

    print("Exploring " + app.getFile() + "." + app.getEntry())
    print("Mode: function")
    result = None

    try:
        test_name_no_ext = os.path.splitext(os.path.basename(filename))[0]
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
            path_priority_weight=path_priority_weight,
        )
        _, return_vals, path = engine.explore(
            max_iters,
            dump_constraints=dump_constraints,
            dump_trace=dump_trace,
            dump_semantics=dump_semantics,
        )
        result = app.executionComplete(return_vals)

        if dot_graph:
            with open(filename + ".dot", "w", encoding="utf-8") as file_obj:
                file_obj.write(path.toDot())

        if dump_constraints:
            print("Dumping constraints...")
        if dump_trace:
            print("Dumping trace...")
        if dump_semantics:
            print("Dumping semantics...")

    except ImportError as exc:
        logging.error(exc)
        return False

    return result


def analyze_input_calls(filename):
    """Analyze input() calls in a Python script to infer input types."""
    try:
        with open(filename, "r", encoding="utf-8") as file_obj:
            content = file_obj.read()

        tree = ast.parse(content, filename=filename)

        class InputCallAnalyzer(ast.NodeVisitor):
            def __init__(self):
                self.calls = []

            def visit(self, node):
                # 为所有节点添加父节点引用
                for child in ast.iter_child_nodes(node):
                    child.parent = node
                super().visit(node)

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id == "input":
                    # 尝试推断输入类型
                    input_type = "int"  # 默认为 int
                    
                    # 查找 input() 调用的使用上下文
                    parent = node
                    while parent:
                        # 检查是否在 int()、float()、str() 调用中
                        if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name):
                            if parent.func.id == "int":
                                input_type = "int"
                                break
                            elif parent.func.id == "float":
                                input_type = "float"
                                break
                            elif parent.func.id == "str":
                                input_type = "str"
                                break
                        # 检查是否在赋值语句中，且右侧是 input() 调用
                        elif isinstance(parent, ast.Assign):
                            # 检查变量是否在其他地方被用作特定类型
                            for target in parent.targets:
                                if isinstance(target, ast.Name):
                                    var_name = target.id
                                    # 搜索变量的使用
                                    class VarUsageFinder(ast.NodeVisitor):
                                        def __init__(self):
                                            self.usage_type = "int"
                                        def visit_Call(self, node):
                                            if isinstance(node.func, ast.Name):
                                                if node.func.id == "int":
                                                    for arg in node.args:
                                                        if isinstance(arg, ast.Name) and arg.id == var_name:
                                                            self.usage_type = "int"
                                                elif node.func.id == "float":
                                                    for arg in node.args:
                                                        if isinstance(arg, ast.Name) and arg.id == var_name:
                                                            self.usage_type = "float"
                                                elif node.func.id == "str":
                                                    for arg in node.args:
                                                        if isinstance(arg, ast.Name) and arg.id == var_name:
                                                            self.usage_type = "str"
                                                elif node.func.id == "len":
                                                    for arg in node.args:
                                                        if isinstance(arg, ast.Name) and arg.id == var_name:
                                                            self.usage_type = "str"
                                        def visit_BinOp(self, node):
                                            # 检查变量是否参与数值运算
                                            if isinstance(node.left, ast.Name) and node.left.id == var_name:
                                                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)):
                                                    self.usage_type = "int"
                                            elif isinstance(node.right, ast.Name) and node.right.id == var_name:
                                                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)):
                                                    self.usage_type = "int"
                                        def visit_Attribute(self, node):
                                            # 检查变量是否访问字符串属性
                                            if isinstance(node.value, ast.Name) and node.value.id == var_name:
                                                # 字符串常见属性
                                                if node.attr in ["strip", "split", "lower", "upper", "replace", "find", "index"]:
                                                    self.usage_type = "str"
                                    finder = VarUsageFinder()
                                    finder.visit(tree)
                                    input_type = finder.usage_type
                                    break
                        parent = getattr(parent, "parent", None)
                    
                    self.calls.append({
                        "node": node,
                        "type": input_type
                    })
                
                self.generic_visit(node)

        analyzer = InputCallAnalyzer()
        analyzer.visit(tree)
        return analyzer.calls
    except Exception:
        return []


def analyze_input_calls(filename):
    """Analyze input() calls in a Python script to infer input types."""
    try:
        with open(filename, "r", encoding="utf-8") as file_obj:
            content = file_obj.read()

        tree = ast.parse(content, filename=filename)

        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                child.parent = parent

        def infer_usage_type(var_name):
            class VarUsageFinder(ast.NodeVisitor):
                def __init__(self):
                    self.usage_type = None

                def _mark(self, usage_type):
                    if self.usage_type is None:
                        self.usage_type = usage_type

                def visit_Call(self, node):
                    if isinstance(node.func, ast.Name):
                        for arg in node.args:
                            if isinstance(arg, ast.Name) and arg.id == var_name:
                                if node.func.id == "int":
                                    self.usage_type = "int"
                                    return
                                if node.func.id == "float":
                                    self.usage_type = "float"
                                    return
                                if node.func.id in {"str", "len"}:
                                    self.usage_type = "str"
                                    return
                    self.generic_visit(node)

                def visit_BinOp(self, node):
                    operands = [node.left, node.right]
                    if any(isinstance(item, ast.Name) and item.id == var_name for item in operands):
                        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Mod, ast.FloorDiv)):
                            self._mark("int")
                        elif isinstance(node.op, ast.Div):
                            self._mark("float")
                    self.generic_visit(node)

                def visit_Attribute(self, node):
                    if isinstance(node.value, ast.Name) and node.value.id == var_name:
                        if node.attr in {
                            "strip",
                            "split",
                            "lower",
                            "upper",
                            "replace",
                            "find",
                            "index",
                            "startswith",
                            "endswith",
                        }:
                            self._mark("str")
                    self.generic_visit(node)

                def visit_Compare(self, node):
                    participants = [node.left] + list(node.comparators)
                    if any(isinstance(item, ast.Name) and item.id == var_name for item in participants):
                        if any(isinstance(item, ast.Constant) and isinstance(item.value, str) for item in participants):
                            self._mark("str")
                    self.generic_visit(node)

            finder = VarUsageFinder()
            finder.visit(tree)
            return finder.usage_type or "str"

        class InputCallAnalyzer(ast.NodeVisitor):
            def __init__(self):
                self.calls = []

            def visit_Call(self, node):
                is_se_literal_eval_pattern = (
                    isinstance(node.func, ast.Name) and
                    node.func.id == "_se_literal_eval" and
                    len(node.args) == 1 and
                    isinstance(node.args[0], ast.Call) and
                    isinstance(node.args[0].func, ast.Name) and
                    node.args[0].func.id == "_se_input"
                )

                if isinstance(node.func, ast.Name) and node.func.id == "input":
                    input_type = "str"
                    is_eval_input = False  # 标记是否是 eval(input()) 模式
                    parent = node

                    while parent:
                        if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name):
                            if parent.func.id == "int":
                                input_type = "int"
                                break
                            if parent.func.id == "float":
                                input_type = "float"
                                break
                            if parent.func.id == "str":
                                input_type = "str"
                                break
                            # 检测 eval(input()) 模式
                            if parent.func.id == "eval":
                                is_eval_input = True
                                input_type = "eval_input"
                                break
                        elif isinstance(parent, ast.Assign):
                            for target in parent.targets:
                                if isinstance(target, ast.Name):
                                    input_type = infer_usage_type(target.id)
                                    break
                            break
                        parent = getattr(parent, "parent", None)

                    self.calls.append({"node": node, "type": input_type, "is_eval_input": is_eval_input})

                elif is_se_literal_eval_pattern:
                    # 识别 _se_literal_eval(_se_input()) 模式
                    self.calls.append({"node": node, "type": "eval_input", "is_eval_input": True})

                self.generic_visit(node)

        analyzer = InputCallAnalyzer()
        analyzer.visit(tree)
        return analyzer.calls
    except Exception:
        return []


def count_input_calls(filename):
    """Count the number of real input() call sites in a Python script."""
    try:
        calls = analyze_input_calls(filename)
        return len(calls)
    except Exception:
        return 0


def run_script_mode(
    filename,
    max_iters=0,
    solver="z3",
    enable_frontier_dedup=False,
    search_strategy="bfs",
    enable_simplify=False,
    enable_prefix_dedup=False,
    max_prefix_length=2,
    enable_incremental=False,
    dump_all_executions=False,
    execution_mode="symbolic",
    concolic_iterations=10,
    concrete_value_strategy="random",
    path_selection_strategy="bfs",
    enable_path_pruning=False,
    enable_hybrid_search=False,
    path_priority_weight=0.5,
    dump_constraints=False,
    dump_trace=False,
    dump_semantics=False,
    dot_graph=False,
    input_schema="",
):
    """Run PyExZ3 in script mode."""
    filename = os.path.abspath(filename)

    from symbolic.script_runner import ScriptRunner

    script_runner = ScriptRunner(filename)
    invocation = script_runner.create_invocation()

    # 处理显式输入 schema 选项
    if input_schema:
        # 解析输入 schema
        input_types = [t.strip() for t in input_schema.split(",")]
        # 验证类型是否有效
        valid_types = ["int", "float", "str"]
        for input_type in input_types:
            if input_type not in valid_types:
                print(f"Warning: Invalid input type '{input_type}', using 'int' instead")
        
        # 根据输入 schema 添加输入
        for index, input_type in enumerate(input_types):
            # 确保类型有效
            if input_type not in valid_types:
                input_type = "int"
            # 根据类型设置默认值
            if input_type == "str":
                default_value = ""
            elif input_type == "float":
                default_value = 0.0
            else:  # int
                default_value = 0
            invocation.add_input(f"input_{index}", default_value, input_type)
        
        print("Exploring script: " + os.path.basename(filename))
        print("Mode: script")
        print(f"Using explicit input schema: {input_schema}")
    else:
        # 使用原来的逻辑，基于代码分析推断输入类型
        input_calls = analyze_input_calls(filename)
        if not input_calls:
            # 没有 input() 调用，添加默认的 int 类型输入
            invocation.add_input("x", 0, "int")
            invocation.add_input("y", 0, "int")
        else:
            # 根据分析结果添加输入，使用推断的类型
            for index, call_info in enumerate(input_calls):
                input_type = call_info.get("type", "int")
                is_eval_input = call_info.get("is_eval_input", False)
                # 根据类型设置默认值
                if input_type == "eval_input":
                    # eval(input()) 需要一个非空字符串，这样 eval() 才能正确处理
                    default_value = "0"
                elif input_type == "str":
                    default_value = ""
                elif input_type == "float":
                    default_value = 0.0
                else:  # int
                    default_value = 0
                invocation.add_input(f"input_{index}", default_value, input_type)

        print("Exploring script: " + os.path.basename(filename))
        print("Mode: script")
        print(f"Found {len(input_calls)} input() call(s)")
    result = None

    try:
        test_name_no_ext = os.path.splitext(os.path.basename(filename))[0]
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
            path_priority_weight=path_priority_weight,
        )
        _, return_vals, path = engine.explore(
            max_iters,
            dump_constraints=dump_constraints,
            dump_trace=dump_trace,
            dump_semantics=dump_semantics,
        )
        result = all(value is None for value in return_vals)

        if dot_graph:
            with open(filename + ".dot", "w", encoding="utf-8") as file_obj:
                file_obj.write(path.toDot())

        if dump_constraints:
            print("Dumping constraints...")
        if dump_trace:
            print("Dumping trace...")
        if dump_semantics:
            print("Dumping semantics...")

    except ImportError as exc:
        logging.error(exc)
        return False

    return result


def run_file(filename, options):
    """Run PyExZ3 on a file with given options."""
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
            dot_graph=options.dot_graph,
            input_schema=options.input_schema,
        )

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
        dot_graph=options.dot_graph,
    )


def parse_options(args=None):
    """Parse command line options."""
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

    parser.add_option("--execution-mode", dest="execution_mode", action="store", help="Execution mode: symbolic|concolic|concrete", default="symbolic")
    parser.add_option("--concolic-iterations", dest="concolic_iterations", type="int", help="Number of concolic execution iterations", default=10)
    parser.add_option("--concrete-value-strategy", dest="concrete_value_strategy", action="store", help="Concrete value generation strategy: random|guided|hybrid", default="random")

    parser.add_option("--path-selection-strategy", dest="path_selection_strategy", action="store", help="Path selection strategy: bfs|dfs|smart", default="bfs")
    parser.add_option("--enable-path-pruning", dest="enable_path_pruning", action="store_true", help="Enable path pruning", default=False)
    parser.add_option("--enable-hybrid-search", dest="enable_hybrid_search", action="store_true", help="Enable hybrid search strategy", default=False)
    parser.add_option("--path-priority-weight", dest="path_priority_weight", type="float", help="Weight for path priority calculation", default=0.5)
    parser.add_option("--input-schema", dest="input_schema", action="store", help="Input schema for script mode, format: type1,type2,... (e.g., int,str,float)", default="")

    options, args = parser.parse_args(args)
    return options, args


def main(args=None):
    """Main function for pyexz3."""
    print("PyExZ3 (Python Exploration with Z3)")

    options, args = parse_options(args)

    if options.logfile != "":
        logging.basicConfig(filename=options.logfile, level=logging.DEBUG)

    if len(args) == 0 or not os.path.exists(args[0]):
        print("Missing app to execute")
        return 1

    result = run_file(args[0], options)

    if result is True:
        return 0
    if result is None:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
