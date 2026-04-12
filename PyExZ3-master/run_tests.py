import os
import re
import sys
import subprocess
from optparse import OptionParser
from sys import platform as _platform

# 确保在正确的目录下运行
def ensure_in_correct_directory():
    """确保脚本在PyExZ3-master目录下运行"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查pyexz3.py是否存在
    pyexz3_path = os.path.join(script_dir, 'pyexz3.py')
    if os.path.exists(pyexz3_path):
        # 切换到脚本目录
        os.chdir(script_dir)
        return True
    else:
        # 尝试在上级目录查找
        parent_dir = os.path.dirname(script_dir)
        pyexz3_path = os.path.join(parent_dir, 'pyexz3.py')
        if os.path.exists(pyexz3_path):
            os.chdir(parent_dir)
            return True
    
    return False

# 在脚本开始时调用
if not ensure_in_correct_directory():
    print("警告: 无法找到pyexz3.py，可能在错误的目录下运行")

# 获取pyexz3.py的绝对路径
pyexz3_abs_path = os.path.abspath("pyexz3.py")
print(f"pyexz3.py绝对路径: {pyexz3_abs_path}")
print(f"当前工作目录: {os.getcwd()}")

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
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.error("Please supply directory of tests")
    sys.exit(1)

# 获取测试目录路径，考虑可能切换了工作目录
test_dir_arg = args[0]
if not os.path.isabs(test_dir_arg):
    # 如果是相对路径，基于当前目录解析
    test_dir = os.path.abspath(test_dir_arg)
else:
    test_dir = test_dir_arg

if not os.path.exists(test_dir):
    print(f"错误: 测试目录不存在: {test_dir}")
    sys.exit(1)
    
if not os.path.isdir(test_dir):
    print("Please provide a directory of test scripts.")
    sys.exit(1)

files = [ f for f in os.listdir(test_dir) if re.search(".py$",f) ]

failed = []
for f in files:
    # execute the python runner for this test
    full = os.path.join(test_dir, f)
    with open(os.devnull, 'w') as devnull:
        solver = "--cvc" if options.cvc else "--z3"
        # 获取当前工作目录（应该在PyExZ3-master目录下）
        current_dir = os.getcwd()
        # 使用绝对路径确保找到pyexz3.py
        pyexz3_path = os.path.join(current_dir, "pyexz3.py")
        if not os.path.exists(pyexz3_path):
            print(f"错误: 找不到pyexz3.py在 {pyexz3_path}")
            sys.exit(1)
        ret = subprocess.call([sys.executable, pyexz3_path, "-m", "25", solver, "--export-path", "--export-frontier", "--export-trace", "--export-corpus", full], 
                              stdout=devnull, stderr=subprocess.PIPE, cwd=current_dir)
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