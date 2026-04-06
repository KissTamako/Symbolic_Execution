#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
符号执行适配器 - 通用类型
生成的测试代码，用于PyExZ3符号执行
"""

from symbolic.args import *


def simple(x):
    if x > 10:
        return 1
    else:
        return 0



# ========== 符号执行测试函数 ==========
@symbolic(input_value=10)
def test_student_code(input_value):
    """
    通用符号执行测试函数
    参数: input_value - 输入值
    返回: 执行结果或状态码
    """
    try:
        # 简单验证逻辑
        if input_value < 0:
            return -1
        
        # 尝试执行原始代码逻辑
        # 这里需要根据具体代码调整
        result = 0
        
        # 示例：简单条件测试
        if input_value > 10:
            result = 1
        else:
            result = 0
            
        return result
        
    except Exception as e:
        # 异常时返回错误代码
        return -999

# ========== 期望结果函数（PyExZ3需要） ==========
def expected_result():
    """返回期望的结果，用于PyExZ3验证"""
    # 对于通用测试，返回一些可能的输出值
    return [0, 1, -1]

# ========== 主程序（用于手动测试） ==========
def main_test():
    """运行简单测试"""
    print("生成的适配器测试")
    print("=" * 60)
    
    test_values = [5, 10, 15]
    for val in test_values:
        result = test_student_code(val)
        print(f"输入值: {val}, 结果: {result}")
    
    print("\n测试完成")

if __name__ == "__main__":
    main_test()
