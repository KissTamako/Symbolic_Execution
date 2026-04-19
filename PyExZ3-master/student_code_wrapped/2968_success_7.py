from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def change(n): #该函数需要返回5个值（可存入列表），即最优方案的总张数及各种钞票的张数，可以使用穷举法
        k=n%25
        n1=int(n/25)
        k1=k%10
        n2=int(k/10)
        k2=k1%5
        n3=int(k1/5)
        k3=k2%1
        n4=int(k2/1)
        n6=n1+n2+n3+n4
        n5=[n6,n1,n2,n3,n4]
        return n5

number=eval(input())
result=change(number)
for x in result:
    print(x,end=" ")


