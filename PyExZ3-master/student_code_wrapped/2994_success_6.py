from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

list1=eval(input())
list1=list(list1)
a,b=eval(input())

if a>=len(list1):
    print("error")
else:
    x1=list1[a]
    while b>0:
        list1.append(int(x1))
        b-=1
    print(list1)




