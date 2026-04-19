from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def zhishu(n):
    f=0
    for i in range(2,n):
        if n%i==0:
            f=1
    if f==0:
        return True
    else:
        return False

n=eval(input())
ls=[]
m=n
i=2
while m>1:
    if m%i==0:
        if zhishu(i):
            ls.append(i)
            m=m/i
    else:
        i+=1
s="%d="%n
ls1=[str(e) for e in ls]
a="*".join(ls1)
print("%s%s"%(s,a))


