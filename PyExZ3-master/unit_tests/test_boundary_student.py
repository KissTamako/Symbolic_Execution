# 边界检查测试学生代码
x = int(input())
y = int(input())

# 测试除法
if y != 0:
    result = x / y
    print(result)

# 测试下标
data = [1, 2, 3, 4, 5]
idx = int(input("索引: "))
if idx >= 0 and idx < len(data):
    print(data[idx])