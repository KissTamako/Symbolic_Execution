a=input()
left="[{("
right="]})"
def jiancha(a):
    result=[]
    for i in a:
        if i in left:
            result.append(i)
        elif i in right:
            if result[-1]==left[right.index(i)]:
                result.pop()
            else:
                return False
    if result!=[]:
        return False
    else:
        return True
print(jiancha(a))


