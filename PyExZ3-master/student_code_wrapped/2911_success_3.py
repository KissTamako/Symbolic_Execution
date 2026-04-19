from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=input()
s=''
for i in a:
    s+=str((int(i)+5)%10)
s1=list(s)
s1.reverse()
b=''.join(s1)
print(b)
