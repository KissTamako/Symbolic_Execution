from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

n=eval(input())
h1=0
for x in list(range(0,int(n)+1)):

      if x%2==0:
            h1 = h1 + x

print(h1)

