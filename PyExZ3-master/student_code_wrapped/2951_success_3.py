from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def matrix(n=2): 
    ls=[['*']*n]*n
    for x in range(n):
        for y in range(n):
            if n==2:
                print(ls[x][y],end='\n' if y==1 else ' ')
            else:
                print(ls[x][y],end='\n' if y==n-1 else ' ')


number=input()
if number=="default":
    matrix() #无实参调用自定义函数
else:
    matrix(eval(number))  #有实参调用自定义函数

