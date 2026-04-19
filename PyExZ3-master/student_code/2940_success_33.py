name=input()
x=name.split()
lst=[]
while name!="quit":
    b=[x[0],x[1]]
    lst.append(b)
    name=input()
    x=name.split()
lst.sort(key=lambda x:x[0])
lst.sort(key=lambda x:x[1])
lb=[]
for i in lst:
    b=i[0]+' '+i[1]
    lb.append(b)
print(lb)
