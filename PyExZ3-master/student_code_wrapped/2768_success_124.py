from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

icard = input()
birthday =  icard[6:10]+"-"+icard[10:12]+"-"+icard[12:14]
mask = mask = icard.replace(icard[6:14],"********")
print(birthday)
print(mask)

