from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

name=input()
x=name.split()
lst=[]
while name!="quit":
    b=[x[0],x[1]]
    lst.append(b)
    name=input()
    x=name.split()
lst.sort(key=lambda x:x[0])
lst.sort(key=lambda x:x[1])
lb=[]
for i in lst:
    b=i[0]+' '+i[1]
    lb.append(b)
print(lb)
