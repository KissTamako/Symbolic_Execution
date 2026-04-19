a=input()
da=0
xiao=0
shu=0
for i in a :
    if i.isdigit():
        shu+=1
    elif i.islower():
        xiao+=1
    elif i.isupper():
        da+=1
print(da)
print(xiao)
print(shu)

