from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def matrix(n=2): 
    if n==2:
        for i in range(2):
            print('* *') 
    else:
        s='* '
        s1=s*int(number)
        s2=str(s1[0:-1])
        for i in range(int(number)):
            print(s2)

number=input()
if number=="default":
    matrix() #无实参调用自定义函数
else:
    matrix(int(number))  #有实参调用自定义函数

