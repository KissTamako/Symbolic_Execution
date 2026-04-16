from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_int, _se_str, _se_float, _se_range


# === 增强型自动生成的包装函数 ===
init_symbolic_inputs([('arg0', None, 'int')])

def _se_wrapper():
    # 自动检测到 1 个输入点
    # 参数: arg0

    arg0 = _se_input('请输入第1个值: ')

# === 特殊函数安全包装 ===

    # --- 学生代码开始 ---
    # 分支测试学生代码
    x = int(input())
    if x > 0:
        print("positive")
    else:
        print("non-positive")
    # --- 学生代码结束 ---

    return result if 'result' in dir() else None

# === 执行包装函数 ===
_se_wrapper()