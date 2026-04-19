from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def GCD(m,n): 
    if n==0:      #递归结束条件
          return m
    else:
          a=n
          n=m%n
          m=a
          return GCD(m,n)

a,b=eval(input())
d=GCD(a,b)  #调用自定义函数
print(d)

