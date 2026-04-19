namelist=[]
while True:
    a=input().split(" ")
    if a != ["quit"]:
        namelist.append(a)
    else:
        break
namelist.sort(key=lambda x:(x[1],x[0]))
finlst=[]
for x in namelist:
    finlst.append(str(x[0]+" "+x[1]))
print(finlst)