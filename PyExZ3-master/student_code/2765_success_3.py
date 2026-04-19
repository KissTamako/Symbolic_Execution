UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
low="abcdefghijklmnopqrstuvwxyz"
dummy=list(input())
for x in dummy:
    if x in UP:
        print(UP[int(25-UP.index(x))],end="")
    elif x in low:
        print(low[int(25-low.index(x))],end="")
    else:
        pass
        print(x,end="")
    