a=input()
x=0
y=0
z=0
for i in a:
    if i.isupper() != 0:
        x += 1
    if i.islower() != 0:
        y+=1
    if i in "1234567890":
        z+=1
    else:
        pass
print(str(x)+"\n"+str(y)+"\n"+str(z))