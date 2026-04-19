from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=list(input())
if len(a) != 18:
    print("Error")
else:
    n=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    x=['1','0','X','9','8','7','6','5','4','3','2']
    s=0
    for i in range(17):
        s=s+int(a[i])*n[i]
    mods=s % 11
    if x[mods]==a[-1]:
        print("Correct")
    else:
        print("Wrong")
