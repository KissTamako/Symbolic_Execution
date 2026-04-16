from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_int, _se_str, _se_float, _se_range


# === 自动生成的包装函数 ===
def _se_wrapper():
    # 自动检测到 2 个 input() 调用
    # 参数: arg0, arg1

    init_symbolic_inputs([('arg0', None, 'int'), ('arg1', None, 'int')])

    # --- 学生代码开始 ---
    # 简单学生代码测试
    x = int(input())
    y = int(input())
    result = x + y
    # --- 学生代码结束 ---

    return result if 'result' in dir() else None