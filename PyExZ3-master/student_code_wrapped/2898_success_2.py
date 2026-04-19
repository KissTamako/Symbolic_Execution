from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

n = eval(input())
i = 0
j = 1
k = 0
s = 1
if n <= 0:
    print("illegal input")
elif type(n) != int:
    print("illegal input")
else:
    while k < n:
        print(s,end = " ")
        s = i + j
        i = j
        j = s
        k += 1
