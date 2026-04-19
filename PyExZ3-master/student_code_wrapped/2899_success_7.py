from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# f = open("in.txt", "r")
# b = {}
# c = []
# for line in f:
#     a = line.split()
#     b[a[0]] = b.get(a[0], 0) + int(a[1])
# for x in b:
#     c.append([x, b[x]])
# c.sort(key=lambda x: len(x[0]))
# c.sort(key=lambda x: x[1], reverse=True)
# f.close()
# f1 = open("out.txt", "w")
# for y in c:
#     f1.write(y[0]+' '+str(y[1])+"\n")
# f1.close()
# def gcd(a, b):
#     while b != 0:
#         a, b = b, a % b
#     return a
#
#
# a = input().split()
# b = gcd(int(a[0]), int(a[1]))
# print(int(a[0]) // b, int(a[1]) // b)
# def lily(a):
#     if int(str(lily)[0])**3 +int(str(lily)[1])**3+int(str(lily)[2])**3 == lily:
#         return True
#     else :
#         return False
# a = int(input())
# flag = 0
# for i in range(100,a):
#     if lily(i):
#         print(i)
#         flag = 1
#     elif flag == 0:
#         print('None')
# def prime_and_yin(a):
#     i = 2
#     factors = []
#     while i * i <= a:
#         if a % i:
#             i += 1
#         else:
#             a //= i
#             factors.append(i)
#     if a > 1:
#         factors.append(a)
#     return factors
#
#
# x = eval(input())
# print(prime_and_yin(x))
# a = input()
# b = 1
# for x in range(len(a) - 1):
#     if a[x] == a[x + 1]:
#         b += 1
#     if x == len(a) - 2:
#         if a[x] != a[x+1]:
#             print(a[x]+a[x+1],end='')
#         else:
#             print(a[x], end='')
#         if b == 1:
#             pass
#         else:
#             print(b, end='')
#     elif a[x] != a[x + 1]:
#         print(a[x], end='')
#         if b == 1:
#             pass
#         else:
#             print(b, end='')
#         b = 1
a = input().split()
n, m = int(a[0]), int(a[1])
c = []
if n>m or n>7 or m <2:
    print("illegal input")
else:
    for x in range(n,m):
        for y in range(n,m):
            for z in range(n,m):
                if int(str(x) + str(y) + str(z)) not in c and x!=y and y!=z and x!=z and len(str(int(str(x) + str(y) + str(z)))) == 3:
                    c.append(int(str(x) + str(y) + str(z)))

    for x in c:
        print(x,end=' ')
