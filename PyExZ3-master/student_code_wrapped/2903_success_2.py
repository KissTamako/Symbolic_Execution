from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def main():
    num = eval(input())
    calculate_e(num)
    print('%.6f'%calculate_e(num))
def calculate_e(num):
    a=1
    for i in range(1,num+1):
        b=i
        for j in range(1,i):
            b*=j
        a=a+1/b
    return a

main()


