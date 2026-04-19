from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

D={}
for i in range(26):
    D[chr(ord("A")+i)]=chr(ord("A")+25-i)
    D[chr(ord("a")+i)]=chr(ord("a")+25-i)

p=input()
c=""
for i in p:
    if "a"<=i<="z" or "A"<=i<="Z":
        c+=D[i]
    else:
        c+=i
print(p)
print(c)               
