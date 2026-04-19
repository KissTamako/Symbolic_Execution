from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def main():
    inword = input()
    print(plural(inword))

def plural(x):
    if x.endswith("s") or x.endswith("x") or x.endswith("ch") or x.endswith("sh") or x.endswith("o"):
        return x+"es"
    elif x.endswith("y"):
        return x[0:len(x)-1]+"ies"
    else:
        return x+"s"

main()

