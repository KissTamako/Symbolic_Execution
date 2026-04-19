from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def yasuo(a):
    b = ""
    c = 1
    for i in range(len(a)-1):
        if a[i]==a[i+1]:
            c = c+1
        elif c==1:
            b = b+a[i]
        else:
            b = b+a[i]+str(c)
            c = 1
    if c!=1:        
        b = b+a[-1]+str(c)
    else:
        b = b+a[-1]
    return b
a = input()
print(yasuo(a))


