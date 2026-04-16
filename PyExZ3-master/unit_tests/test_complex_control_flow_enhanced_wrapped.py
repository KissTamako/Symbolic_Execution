
# === 增强型自动生成的包装函数 ===
def _se_wrapper(x):
    return outer(x)

# === 特殊函数安全包装 ===

# === 原代码开始 ===
# 嵌套函数和复杂控制流测试

# 测试1: 嵌套函数
def outer(x):
    def inner(y):
        return y * 2
    return inner(x) + 1

# 测试2: lambda 表达式
def use_lambda(n):
    func = lambda x: x * n
    return func(5)

# 测试3: 生成器
def generator_test(n):
    for i in range(n):
        yield i * 2

# 测试4: 正常函数
def normal(x):
    return x + 1
# === 原代码结束 ===