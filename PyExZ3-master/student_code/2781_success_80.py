id=list(input())
if len(id)!=18:
    print("Error")
else:
    n=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    last=['1','0','X','9','8','7','6','5','4','3','2']
    sum=0
    for i in range(len(n)):
        sum+=int(id[i])*n[i]
    lasti=sum%11
    if last[lasti] == id[-1]:
        print("Correct")
    else:
        print("Wrong")

