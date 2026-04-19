from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def prime(n): #该函数有两个返回值，分别是素数个数和素数的和
        a=[]
        b=[]
        for i in range(2,n):
                for x in range(2,i):
                    if i%x==0:
                        break
                else:
                    a.append(i)
        b.append(len(a))
        b.append(sum(a))
        return b


number=eval(input())
result=prime(number)
print(result[0],result[1])

