from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

namelist=[]
while True:
    a=input().split(" ")
    if a != ["quit"]:
        namelist.append(a)
    else:
        break
namelist.sort(key=lambda x:(x[1],x[0]))
finlst=[]
for x in namelist:
    finlst.append(str(x[0]+" "+x[1]))
print(finlst)