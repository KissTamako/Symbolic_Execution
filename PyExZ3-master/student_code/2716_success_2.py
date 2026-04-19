di_result={}
def findMax(ls):
    for x in list(range(len(ls))):
        if ls[x] == max(ls):
            di_result[x] = max(ls)
            break
        else:
            pass
    return di_result

ls=eval(input())
result=findMax(ls)
for  i,j  in  result.items():
          print(str(i)+":"+str(j))


