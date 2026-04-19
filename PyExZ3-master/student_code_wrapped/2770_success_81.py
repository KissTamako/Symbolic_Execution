from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

word1 = input().strip()
word2 = input().strip()
if sorted(word1) == sorted(word2):
    print(True)
else :
    print(False)

