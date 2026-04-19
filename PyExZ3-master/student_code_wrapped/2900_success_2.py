from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

n=eval(input())
a=str(n)
m=[]
if a.count('.')==1 or n<=0:
    print("illegal input")
else:
    for i in range(2,n):
        for x in range(2,i):
            if i%x==0:
                break
        else:
            if i==int(str(i)[::-1]):
                print(i,end=" ")


