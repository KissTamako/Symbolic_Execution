#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单正确的学生代码示例 - 类似于test/simple.py
用于验证PyExZ3对正确代码的处理能力
"""

from symbolic.args import symbolic

@symbolic(x=10)
def simple_correct(x):
    """
    简单函数，类似test/simple.py
    如果x+1 > 10，返回42，否则返回43
    """
    if (x + 1 > 10):
        return 42
    else:
        return 43

def expected_result():
    """
    期望的结果：函数可能返回的所有值
    注意：返回列表中的元素必须是可哈希的（不能是列表）
    """
    return [42, 43]

def main():
    """简单测试"""
    print("测试简单正确的学生代码")
    print("函数: simple_correct(x)")
    print("逻辑: if (x+1 > 10) return 42 else return 43")
    print()
    
    # 测试几个具体值
    test_values = [5, 9, 10, 11]
    for x in test_values:
        result = simple_correct(x)
        print(f"  x={x}: 返回值={result}")
    
    print("\n期望的结果:", expected_result())
    print("注意：所有可能的返回值是42和43")

if __name__ == "__main__":
    main()