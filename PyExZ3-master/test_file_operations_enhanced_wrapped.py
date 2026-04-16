from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_int, _se_str, _se_float, _se_range


# === 增强型自动生成的包装函数 ===
def _se_wrapper():
    # 自动检测到 1 个输入点
    # 参数: arg0

    arg0 = _se_input('请输入第1个值: ')

    return main()

# === 特殊函数安全包装 ===

# === 原代码开始 ===
# 包含文件操作的学生代码测试
def read_file():
    f = open('test.txt', 'r')
    content = f.read()
    f.close()
    return content

def main():
    x = int(input())
    print(x)

# === 原代码结束 ===