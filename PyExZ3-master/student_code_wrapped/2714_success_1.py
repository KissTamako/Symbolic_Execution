from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

s={"A":"A","B":"B","C":"C","D":"D","E":"E"}
n=eval(input())
if n>=90:
    print(s["A"])
elif n>=80 and n<90:
    print(s["B"])
elif n>=70 and n<80:
    print(s["C"])
elif n>=60 and n<70:
    print(s["D"])
else:
    print(s["E"])


