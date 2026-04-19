from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=input()
b=[]
for i in a:
    b.append(i)
for i in range(len(b)):
    if b[i] in 'qwertyuiopasdfghjklzxcvbnm':
        b[i]=chr(96+27-(ord(b[i])-96))
    elif b[i] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        b[i]=chr(63+27-(ord(b[i])-65))
print(a)
print(''.join(b))

