a=eval(input())
x=0
y=0
z=0
if a<153:
    print("none")
else:
    for i in range(100,a+1):
        x=i%10
        y=int(((i-x)/10)%10)
        z=(i-x-y*10)//100
        if (x**3)+(y**3)+(z**3)==i and i<1000:
            print(i)


