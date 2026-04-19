h = eval(input())
N = eval(input())
ls = [h, h]
for i in range(2, N):
    h = h / 2
    ls.append(h)
print('%.2f' % sum(ls))