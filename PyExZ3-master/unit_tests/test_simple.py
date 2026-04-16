# Test file for PyExZ3

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from symbolic.args import symbolic

@symbolic(a=10, b="test")
def test_function(a, b):
    if a > 5:
        if len(b) > 3:
            return "Both conditions met"
        else:
            return "First condition met, second not"
    else:
        return "First condition not met"

def expected_result():
    return ["Both conditions met", "First condition met, second not", "First condition not met"]
