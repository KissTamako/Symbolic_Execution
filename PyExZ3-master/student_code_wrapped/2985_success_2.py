from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

student = eval(input())
info = tuple(student[1:3])

avg = sum(student[-1])/len(student[-1])

print(info)
print("%.2f"%avg)

