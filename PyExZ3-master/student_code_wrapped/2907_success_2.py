from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def main():
    N,M = map(int,input().split())
    calculate_capital(N,M)
    print('%.4f'%calculate_capital(N,M))
def calculate_capital(N,M):
        a=N*(1.003**M)
        return a

main()



