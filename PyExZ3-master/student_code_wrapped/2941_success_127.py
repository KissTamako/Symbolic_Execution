from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def count_foreign(ids):

        a = 0
        for i in ids:
            if len(i) ==9:
                a += 1
        return a

origin=input().split()
print(count_foreign(origin))

