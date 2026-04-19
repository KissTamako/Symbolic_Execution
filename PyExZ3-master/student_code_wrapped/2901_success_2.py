from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

i=0
b=0
d=0
while True:
    b=input()
    if b=="#":
        break
    else:
        a=eval(b)
        i=i+a
        d=d+1
print(d,i)


