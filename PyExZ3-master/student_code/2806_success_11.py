b=list(input())
m=""
for i in range(len(b)):
    if i>0 and b[i] ==b[i-1]:
        continue
    a=b[i:]
    count=0
#     if a.count(b[i])>1 and i<len(b)-1 and  b[i]==b[i+1]:
#         m=m+str(b[i])+str(a.count(b[i]))       
#     else:
#         m=m+b[i]
# print(m)
    for x in a:
        if x==b[i]:
            count+=1
        else:
            break
    if count>1:
        print("{}{}".format(b[i],count),end="")
    else:
        print(b[i],end="")

