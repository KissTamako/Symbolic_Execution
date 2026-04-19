lst = list(eval(input()))
n,m = eval(input())
if abs(n) > len(lst):
    print("error")
else:
    lst2 = [lst[n]]*m
    lst.extend(lst2)
    print(lst)
