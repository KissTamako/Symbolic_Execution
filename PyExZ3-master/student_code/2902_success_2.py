a=0
d=1
f=2
g=0
n=eval(input())
while True:
    b=f/d
    g=g+b
    f=d+f
    d=f-d
    a=a+1
    if a==n:
        break
print('%.4f'%g)

