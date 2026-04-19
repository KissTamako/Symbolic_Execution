str = input()
a = str.split(' ')
# print(a)
num = input()
b = num.split()
a[int(b[0])], a[int(b[1])] = a[int(b[1])], a[int(b[0])]
print(a)
