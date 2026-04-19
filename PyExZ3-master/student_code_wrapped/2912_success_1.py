from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

n=eval(input())
sum1=0
while n>0:
  sum1+=n%10
  n=int(n/10)
print(sum1)

