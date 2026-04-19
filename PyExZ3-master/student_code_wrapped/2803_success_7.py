from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def main():
    s = input()
    ch = input()
    print(count(s,  ch))


def count(s, ch):
    for i in range(len(s)):
        if ch == s[i]:
            return i

    return None


main()

