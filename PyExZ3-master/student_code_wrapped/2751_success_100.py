from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def  fibo(n):
       if n<=2:
             return 1
       else:
              return fibo(n-1) +fibo(n-2)  

n=int(input())
print(fibo(n))


