# Copyright: see copyright.txt

import os
import sys
import logging
import traceback
from optparse import OptionParser

# 检查CVC4是否可用（可选依赖）
def check_cvc4_available():
    try:
        import CVC4
        return True
    except ImportError:
        return False

CVC4_AVAILABLE = check_cvc4_available()

from symbolic.loader import *
from symbolic.explore import ExplorationEngine

print("PyExZ3 (Python Exploration with Z3)")

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

usage = "usage: %prog [options] <path to a *.py file>"
parser = OptionParser(usage=usage)

parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file", default="")
parser.add_option("-s", "--start", dest="entry", action="store", help="Specify entry point", default="")
parser.add_option("-g", "--graph", dest="dot_graph", action="store_true", help="Generate a DOT graph of execution tree")
parser.add_option("-m", "--max-iters", dest="max_iters", type="int", help="Run specified number of iterations", default=0)
parser.add_option("--cvc", dest="cvc", action="store_true", help="Use the CVC SMT solver instead of Z3", default=False)
parser.add_option("--z3", dest="cvc", action="store_false", help="Use the Z3 SMT solver")

(options, args) = parser.parse_args()

# 检查是否选择了CVC4但CVC4不可用
if options.cvc and not CVC4_AVAILABLE:
    print("ERROR: CVC4 solver is not available on this system.")
    print("Please install CVC4 with Python bindings or use the default Z3 solver (remove --cvc flag).")
    print("You can install CVC4 from: https://cvc4.github.io/")
    print("Or use Z3 which is already supported by this installation.")
    sys.exit(1)

if not (options.logfile == ""):
	logging.basicConfig(filename=options.logfile,level=logging.DEBUG)

if len(args) == 0 or not os.path.exists(args[0]):
	parser.error("Missing app to execute")
	sys.exit(1)

solver = "cvc" if options.cvc else "z3"

filename = os.path.abspath(args[0])
	
# Get the object describing the application
app = loaderFactory(filename,options.entry)
if app == None:
	sys.exit(1)

print ("Exploring " + app.getFile() + "." + app.getEntry())

result = None
try:
	engine = ExplorationEngine(app.createInvocation(), solver=solver)
	generatedInputs, returnVals, path = engine.explore(options.max_iters)
	# check the result
	result = app.executionComplete(returnVals)

	# output DOT graph
	if (options.dot_graph):
		file = open(filename+".dot","w")
		file.write(path.toDot())	
		file.close()

except ImportError as e:
	# createInvocation can raise this
	logging.error(e)
	sys.exit(1)

if result == None or result == True:
	sys.exit(0);
else:
	sys.exit(1);	
