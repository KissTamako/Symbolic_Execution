from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def  stuid(data2):
        a=[]
        for i in data2:
            a.append(i[0:8])
        return a

data1=input().split()
student_id=stuid(data1)
for x in student_id:
    print(x,end=" ")




