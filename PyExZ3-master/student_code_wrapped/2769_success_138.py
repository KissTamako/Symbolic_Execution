from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a = input()
print(a)
for x in a:
    if x.isalpha():
        if x.islower():
            x=chr(25-ord(x)+ord('a')*2)
            print(x,end='')
        else:
            x=chr(25-ord(x)+ord('A')*2)
            print(x,end='')
    else:
        print(x,end='')
