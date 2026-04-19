from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

student = eval(input())
info = (student[1],student[2])
avg = sum(student[5])/len(student[5])
print(info)
print("%.2f"%avg)

