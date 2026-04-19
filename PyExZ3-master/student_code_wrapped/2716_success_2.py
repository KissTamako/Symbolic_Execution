from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

di_result={}
def findMax(ls):
    for x in list(range(len(ls))):
        if ls[x] == max(ls):
            di_result[x] = max(ls)
            break
        else:
            pass
    return di_result

ls=eval(input())
result=findMax(ls)
for  i,j  in  result.items():
          print(str(i)+":"+str(j))


