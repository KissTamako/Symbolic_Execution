from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def shu(a):
    if a==(int(str(a)[0])**3+int(str(a)[1])**3+int(str(a)[2])**3):
        return True
    return False
n=eval(input())
m=0
for x in range(100,n+1):
    if shu(x):
        print(x)
        m=1
if m==0:
    print('none')

