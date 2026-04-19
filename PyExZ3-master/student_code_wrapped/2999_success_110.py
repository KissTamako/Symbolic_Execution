from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=list(map(str,input().split()))
b,c=map(int,input().split())
d=a.copy()
d[b]=a[c]
d[c]=a[b]
print(d)
