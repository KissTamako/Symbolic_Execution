from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

line = input()
for s in line:
    if s.isalpha():
        if s.islower():
               print(s.upper(),end='')          
        else:
               print(s.lower(), end='')
    else:
          print(s,end='')


