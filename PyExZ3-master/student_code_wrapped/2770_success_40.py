from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

s1 = str(input())
s2 = str(input())
s1list = list(s1)
s2list = list(s2)
s1list.sort()
s2list.sort()
if s1list == s2list:
    print(True)
else:
    print(False)









