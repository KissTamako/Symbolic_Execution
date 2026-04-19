from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a=input()
left="[{("
right="]})"
def jiancha(a):
    result=[]
    for i in a:
        if i in left:
            result.append(i)
        elif i in right:
            if result[-1]==left[right.index(i)]:
                result.pop()
            else:
                return False
    if result!=[]:
        return False
    else:
        return True
print(jiancha(a))


