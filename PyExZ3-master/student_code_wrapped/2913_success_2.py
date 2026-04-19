from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

n=int(input())
j=1
b=-1
flag=False
while n>0:
  if n%10==5:
    print(j)
    flag=True
  n=n//10
  j+=1
if not flag:
  print(b)

