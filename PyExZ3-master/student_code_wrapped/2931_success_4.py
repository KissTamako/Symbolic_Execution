from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def medium(number2):
    number2.sort()
    x=len(number2)//2
    if len(number2)/2!=x:
        med=number2[x]
    else:
        med=(number2[x]+number2[x-1])/2
    return med

origin=input().split()
number1=[eval(x) for x in origin]
print("%.2f"%medium(number1))

