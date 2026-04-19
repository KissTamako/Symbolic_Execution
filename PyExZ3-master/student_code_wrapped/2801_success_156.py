from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

s=input()
n=0
for i in s:
    if i in "1234567890":
        n=n+1
        break
for i in s:
    if "a"<=i<="z":
        n=n+1
        break
for i in s:
    if "A"<=i<="Z":
        n=n+1
        break
for i in s:
    if i in "~!@#$%^&*()_=-/,.?<>;:[]{ }|\ ":
        n=n+1
        break
if len(s)>=8:
    n=n+1
print(n)
