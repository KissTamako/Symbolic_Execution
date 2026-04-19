x1=input()
a,b=x1.split(" ")
b=int(b)
a=int(a)
list=[]
if b-a<3 or b<a or b<0 or a<0 or a>9 or b>9:
    print("illegal input")
else:
    for i in range(a,b):
        for j in range(a,b):
            for d in range(a,b):
                if i!=j and j!=d and i!=d:
                    if i==0:
                        pass
                    else:
                        list.append(str(i)+str(j)+str(d))
    print(*list)

