n=eval(input())
a=str(n)
m=[]
if a.count('.')==1 or n<=0:
    print("illegal input")
else:
    for i in range(2,n):
        for x in range(2,i):
            if i%x==0:
                break
        else:
            if i==int(str(i)[::-1]):
                print(i,end=" ")
            

