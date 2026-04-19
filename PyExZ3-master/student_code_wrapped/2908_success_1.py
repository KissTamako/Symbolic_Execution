from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

n=int(input())
print('%d='%n,end='')
while n>1:
    for i in range(2,n+1):
        if n%i==0:
            n=int(n/i)
            if n==1:
                print('%d'%i,end='')
            else:
                print('%d*'%i,end='')
            break
print()

