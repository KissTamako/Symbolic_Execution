import math

def float_functions(x):
    # 测试三角函数
    sin_val = math.sin(x)
    cos_val = math.cos(x)
    
    # 测试其他数学函数
    if x >= 0:
        sqrt_val = math.sqrt(x)
    else:
        sqrt_val = 0
    
    exp_val = math.exp(x)
    
    # 测试条件判断，确保能够覆盖所有返回值
    if x > 2:
        return 1
    elif x > 0:
        return 2
    elif x > -2:
        return 3
    else:
        return 4

def expected_result():
    return [1, 2, 3, 4]
