from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=input()
da=0
xiao=0
shu=0
for i in a :
    if i.isdigit():
        shu+=1
    elif i.islower():
        xiao+=1
    elif i.isupper():
        da+=1
print(da)
print(xiao)
print(shu)

