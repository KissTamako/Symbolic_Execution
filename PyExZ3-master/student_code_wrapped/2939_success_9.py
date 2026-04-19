from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def compute_variance(number2):
    ave=sum(number2)/len(number2)
    mySum=0
    for x in number2:
        mySum+=(x-ave)**2
    variance=mySum/len(number2)
    return variance

origin=input().split()
number1=[eval(x) for x in origin]
print("%.2f"%compute_variance(number1))

