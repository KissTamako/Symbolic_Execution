from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def add_id(data2):
    for x in range(len(data2)):
        data2[x]=str(data2[x])
        data2[x]="20"+data2[x]
    return data2    

data1=input().split()
result=add_id(data1)
for x in result:
    print(x,end=" ")

