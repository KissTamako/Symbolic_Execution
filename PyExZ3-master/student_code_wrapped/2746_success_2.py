from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=input()
x=0
y=0
z=0
for i in a:
    if i.isupper() != 0:
        x += 1
    if i.islower() != 0:
        y+=1
    if i in "1234567890":
        z+=1
    else:
        pass
print(str(x)+"\n"+str(y)+"\n"+str(z))