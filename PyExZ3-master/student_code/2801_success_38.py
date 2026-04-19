s=input()
count=0
if len(s)>=8:
    count+=1
for i in "abcdefghijklmnopqrstuvwxyz":
    if i in s:
        count+=1
        break
for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    if j in s:
        count+=1
        break
for x in "0123456789":
    if x in s:
        count+=1
        break
for y in ["~","!","@","#","$","%","^","&","*","(",")","_","=","-","/",",",".","?","<",">",";",":","[","]","{","}","|","\\"]:
    if y in s:
        count+=1
        break
print(count)

