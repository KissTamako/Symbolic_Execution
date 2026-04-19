h = eval(input())
n = eval(input())
s = h
for i in range(n - 1):
    s += h * 0.5 ** i
print('%.2f' % s)