from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def main():
    a = input()
    print(strreduce(a))

def strreduce(a):
    a=list(a)
    b=[]
    for i in a:
        if i not in b:
            b.append(i)
    s=("".join(map(str,b)))
    return(s)




main()

