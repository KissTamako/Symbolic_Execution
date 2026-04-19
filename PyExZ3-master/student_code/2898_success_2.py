n = eval(input())
i = 0
j = 1
k = 0
s = 1
if n <= 0:
    print("illegal input")
elif type(n) != int:
    print("illegal input")
else:
    while k < n:
        print(s,end = " ")
        s = i + j
        i = j
        j = s
        k += 1
