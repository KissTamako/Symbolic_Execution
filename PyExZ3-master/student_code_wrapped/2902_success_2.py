from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=0
d=1
f=2
g=0
n=eval(input())
while True:
    b=f/d
    g=g+b
    f=d+f
    d=f-d
    a=a+1
    if a==n:
        break
print('%.4f'%g)

