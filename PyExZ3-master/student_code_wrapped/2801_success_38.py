from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

s=input()
count=0
if len(s)>=8:
    count+=1
for i in "abcdefghijklmnopqrstuvwxyz":
    if i in s:
        count+=1
        break
for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    if j in s:
        count+=1
        break
for x in "0123456789":
    if x in s:
        count+=1
        break
for y in ["~","!","@","#","$","%","^","&","*","(",")","_","=","-","/",",",".","?","<",">",";",":","[","]","{","}","|","\\"]:
    if y in s:
        count+=1
        break
print(count)

