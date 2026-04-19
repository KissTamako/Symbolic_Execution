def findMax(a):
    b=max(a)
    c=a.index(b)
    d={c:b}
    return d

ls=eval(input())
result=findMax(ls)
for  i,j  in  result.items():
          print(str(i)+":"+str(j))


