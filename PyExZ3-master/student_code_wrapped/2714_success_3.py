from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=int(input())
if 90<=a<=100:
    print("A")
elif 80<=a<90:
    print("B")
elif 70<=a<80:
    print("C")
elif 60<=a<70:
    print("D")
else:
    print("E")
