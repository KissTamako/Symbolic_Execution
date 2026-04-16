import os
import re
import sys
import subprocess
from optparse import OptionParser
from sys import platform as _platform

class bcolors:
    SUCCESS = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'

def myprint(color, s, *args):
  if _platform != "win32" and sys.stdout.isatty():
    print(color, s, bcolors.ENDC, *args)
  else:
    print(*args)

usage = "usage: %prog [options] <test directory>"
parser = OptionParser()
parser.add_option("--cvc", dest="cvc", action="store_true", help="Use the CVC SMT solver instead of Z3", default=False)
parser.add_option("--z3", dest="cvc", action="store_false", help="Use the Z3 SMT solver")
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
(options, args) = parser.parse_args()

if len(args) == 0 or not os.path.exists(args[0]):
    parser.error("Please supply directory of tests")
    sys.exit(1)
    
test_dir = os.path.abspath(args[0])

if not os.path.isdir(test_dir):
    print("Please provide a directory of test scripts.")
    sys.exit(1)

files = [ f for f in os.listdir(test_dir) if re.search(".py$",f) ]

failed = []
for f in files:
	# execute the python runner for this test
        full = os.path.join(test_dir, f)
        solver = "--cvc" if options.cvc else "--z3"
        
        # 构建命令参数
        cmd_args = [sys.executable, "pyexz3.py", "--max-iters=25", solver]
        
        # 检查是否是脚本模式的测试文件
        # 脚本模式的测试文件通常包含 input() 调用，或者文件名以 input_ 开头
        filename = os.path.basename(full)
        with open(full, 'r', encoding='utf-8') as file_obj:
            content = file_obj.read()
            has_input_call = 'input(' in content
            starts_with_input = filename.startswith('input_')
            is_script_mode = has_input_call or starts_with_input
        
        if is_script_mode:
            cmd_args.append("--mode")
            cmd_args.append("script")
        
        # 添加导出选项
        if options.dump_constraints:
            cmd_args.append("--dump-constraints")
        if options.dump_trace:
            cmd_args.append("--dump-trace")
        if options.dump_semantics:
            cmd_args.append("--dump-semantics")
        
        # 添加优化选项
        if options.enable_unsat_cache:
            cmd_args.append("--enable-unsat-cache")
        if options.enable_frontier_dedup:
            cmd_args.append("--enable-frontier-dedup")
        cmd_args.append(f"--search-strategy={options.search_strategy}")
        if options.enable_simplify:
            cmd_args.append("--enable-simplify")
        if options.enable_prefix_dedup:
            cmd_args.append("--enable-prefix-dedup")
        cmd_args.append(f"--max-prefix-length={options.max_prefix_length}")
        if options.enable_incremental:
            cmd_args.append("--enable-incremental")
        if options.dump_all_executions:
            cmd_args.append("--dump-all-executions")
        
        # 添加测试文件名
        cmd_args.append(full)
        
        print(f"\n=== Running test: {f} ===")
        ret = subprocess.call(cmd_args)
        if (ret == 0):
            myprint(bcolors.SUCCESS, "✓", "Test " + f + " passed.")
        else:
            failed.append(f)
            myprint(bcolors.FAIL, "✗", "Test " + f + " failed.")

if failed != []:
	print("RUN FAILED")
	print(failed)
	sys.exit(1)
else:
	sys.exit(0)