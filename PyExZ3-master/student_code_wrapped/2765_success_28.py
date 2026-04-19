from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

sr=input()
s=''
for ch in sr:
    if ch>="A" and ch<="Z":
        s+=chr(ord("Z")-(ord(ch)-ord('A')))
    elif ch>='a' and ch<='z':
        s+=chr(ord('z')-(ord(ch)-ord('a')))
    else:
        s+=ch
print(s)

