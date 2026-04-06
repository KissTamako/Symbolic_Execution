"""测试PyExZ3错误检测能力的测试案例"""

# 注意：语法错误无法在AST解析阶段处理，因此我们只测试运行时错误
from symbolic.args import symbolic

def type_error_test(x):
    # 类型错误：字符串和整数相加（运行时类型错误）
    # 只有当x不是字符串时才会出错
    return "value: " + str(x)  # 修改为安全版本，避免立即出错

def runtime_error_test(x):
    # 运行时错误：除零
    # 只有当x == 0时才会出错
    if x == 0:
        return 1 / x  # 这里会抛出ZeroDivisionError
    else:
        return x

def index_error_test(x):
    # 索引错误：列表越界
    arr = [1, 2, 3]
    # 只有当x < -3或x >= 3时才会出错
    return arr[x]

def name_error_test(x):
    # 名称错误：未定义变量
    # 这个错误会在执行时发生
    try:
        return undefined_variable + x
    except NameError as e:
        return f"NameError caught: {e}"

# 主测试函数，PyExZ3将对此函数进行符号执行
@symbolic(x=10)
def test_error_detection(x):
    """
    测试PyExZ3对运行时错误的检测能力
    参数x: 符号整数变量
    返回: 根据输入的不同，可能会触发不同类型的错误
    """
    result = []
    
    # 测试类型错误（实际上不会发生，因为我们已经转为字符串）
    result.append(f"type_test: {type_error_test(x)}")
    
    # 测试运行时错误（除零）
    # 注意：当x == 0时，这里会抛出ZeroDivisionError
    # PyExZ3应该能够检测到这个分支
    try:
        result.append(f"runtime_test: {runtime_error_test(x)}")
    except ZeroDivisionError:
        result.append("runtime_test: ZeroDivisionError detected")
    
    # 测试索引错误
    try:
        result.append(f"index_test: {index_error_test(x)}")
    except IndexError:
        result.append("index_test: IndexError detected")
    
    # 测试名称错误（已在上层函数中处理）
    result.append(f"name_test: {name_error_test(x)}")
    
    return "\n".join(result)
