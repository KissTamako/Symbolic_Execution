from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

lst1=list(input())
shuzi=0
zimu=0
da=0
qita=0
for i in lst1:
    if (ord(i)>=65 and ord(i)<=90):
        zimu+=1
    elif ord(i)>=48 and ord(i)<=57:
        shuzi+=1
    elif (ord(i)>=97 and ord(i)<=122):
        da+=1
    else:
        qita+=1
print(zimu)
print(da)
print(shuzi)

















