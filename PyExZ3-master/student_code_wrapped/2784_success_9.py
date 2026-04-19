from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def main():
    inword = input()
    print(plural(inword))

def plural(a):
    if a[-1] in 'sx' or a[-2:] in ['sh','ch']:
        return a+'es'
    elif a[-1] in 'o':
        return a+'es'
    elif a[-1] in 'y':
        return a[0:-1]+'ies'
    else:
        return a+'s'


main()

