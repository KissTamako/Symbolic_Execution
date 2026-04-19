from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=eval(input())
x=0
y=0
z=0
if a<153:
    print("none")
else:
    for i in range(100,a+1):
        x=i%10
        y=int(((i-x)/10)%10)
        z=(i-x-y*10)//100
        if (x**3)+(y**3)+(z**3)==i and i<1000:
            print(i)


