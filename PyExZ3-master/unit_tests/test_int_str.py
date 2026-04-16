# Test file for PyExZ3 int and str symbolic execution

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from symbolic.args import symbolic

@symbolic(a=10, b="hello")
def test_int_str(a, b):
    result = 0
    if a > 5:
        result += 1
        if len(b) > 3:
            result += 1
            if b.startswith("h"):
                result += 1
    elif a < 0:
        result -= 1
    else:
        result = 0
    return result

def expected_result():
    return [3, 2, 0, -1]
