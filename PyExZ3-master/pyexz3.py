# Copyright: see copyright.txt

import os
import sys
import logging
import traceback
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine

print("PyExZ3 (Python Exploration with Z3)")

# Get the directory of the current file
try:
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
except NameError:
    # If __file__ is not defined (e.g., when executed via exec), use the current working directory
    current_dir = os.path.abspath(os.getcwd())
sys.path = [current_dir] + sys.path

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

(options, args) = parser.parse_args()

if not (options.logfile == ""):
	logging.basicConfig(filename=options.logfile,level=logging.DEBUG)

if len(args) == 0 or not os.path.exists(args[0]):
	parser.error("Missing app to execute")
	sys.exit(1)

solver = "cvc" if options.cvc else "z3"

filename = os.path.abspath(args[0])	

# Get the object describing the application
if options.mode == "script":
	# Use ScriptRunner for script mode
	from symbolic.script_runner import ScriptRunner
	script_runner = ScriptRunner(filename)
	invocation = script_runner.create_invocation()
	# Add symbolic inputs
	invocation.add_input("x", 0)
	invocation.add_input("y", 0)
	print ("Exploring script: " + os.path.basename(filename))
	print ("Mode: " + options.mode)
	result = None
try:
	# 为每个测试创建独立的输出目录
	test_name = os.path.basename(filename)
	test_name_no_ext = os.path.splitext(test_name)[0]
	output_dir = os.path.join(current_dir, "outputs", test_name_no_ext)
	os.makedirs(output_dir, exist_ok=True)
	
	if options.mode == "script":
		engine = ExplorationEngine(
			invocation, 
			solver=solver, 
			output_dir=output_dir,
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
			path_priority_weight=options.path_priority_weight
		)
		generatedInputs, returnVals, path = engine.explore(
			options.max_iters,
			dump_constraints=options.dump_constraints,
			dump_trace=options.dump_trace,
			dump_semantics=options.dump_semantics
		)
		# For script mode, we just check if the script executed without errors
		result = True
	else:
		# Use Loader for function mode
		app = loaderFactory(filename,options.entry)
		if app == None:
			sys.exit(1)
		print ("Exploring " + app.getFile() + "." + app.getEntry())
		print ("Mode: " + options.mode)
		engine = ExplorationEngine(
			app.createInvocation(), 
			solver=solver, 
			output_dir=output_dir,
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
			path_priority_weight=options.path_priority_weight
		)
		generatedInputs, returnVals, path = engine.explore(
			options.max_iters,
			dump_constraints=options.dump_constraints,
			dump_trace=options.dump_trace,
			dump_semantics=options.dump_semantics
		)
		# check the result
		result = app.executionComplete(returnVals)

	# output DOT graph
	if (options.dot_graph):
		file = open(filename+".dot","w")
		file.write(path.toDot())	
		file.close()

	# Handle dump options
	if options.dump_constraints:
		print("Dumping constraints...")
		# TODO: Implement constraint dumping
	
	if options.dump_trace:
		print("Dumping trace...")
		# TODO: Implement trace dumping
	
	if options.dump_semantics:
		print("Dumping semantics...")
		# TODO: Implement semantic dumping

except ImportError as e:
	# createInvocation can raise this
	logging.error(e)
	sys.exit(1)

if __name__ == "__main__":
	if result == None or result == True:
		sys.exit(0);
	else:
		sys.exit(1);

def main():
	"""Main function for pyexz3"""
	global result
	if result == None or result == True:
		sys.exit(0);
	else:
		sys.exit(1);	
