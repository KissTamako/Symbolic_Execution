from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
low="abcdefghijklmnopqrstuvwxyz"
dummy=list(input())
for x in dummy:
    if x in UP:
        print(UP[int(25-UP.index(x))],end="")
    elif x in low:
        print(low[int(25-low.index(x))],end="")
    else:
        pass
        print(x,end="")
