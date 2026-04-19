a = input()
i = 0
while i < len(a):
    if a[i] in ['1','2','3','4','5','6','7','8','9','0']:
        a = a[0:i]+a[i+1:]
        i = i - 1
    i = i + 1
print(a)

