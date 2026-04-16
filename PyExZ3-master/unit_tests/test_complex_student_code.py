# 复杂学生代码示例 - 包含多种输入输出和特殊函数
import random

def calculate(x, y):
    if x > 0:
        if y > 0:
            result = x + y
        else:
            result = x - y
    else:
        if y > 0:
            result = x * y
        else:
            try:
                result = x / y
            except ZeroDivisionError:
                result = 0

    return result

# 主程序
a = int(input())
b = int(input())
operation = input("选择操作: ")

if operation == "add":
    print(calculate(a, b))
elif operation == "multiply":
    print(calculate(a, b))
else:
    print("未知操作")

# 测试边界条件
data = [1, 2, 3, 4, 5]
idx = int(input("输入索引: "))
if idx >= 0 and idx < len(data):
    print(data[idx])
else:
    print("索引越界")