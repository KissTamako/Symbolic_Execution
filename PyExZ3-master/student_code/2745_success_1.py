a=input().split(" ")
a.sort(key=lambda x:ascii(x))
for x in a:
    print(x,end=" ")

