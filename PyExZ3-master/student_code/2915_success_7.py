def shu(a):
    if a==(int(str(a)[0])**3+int(str(a)[1])**3+int(str(a)[2])**3):
        return True
    return False
n=eval(input())
m=0
for x in range(100,n+1):
    if shu(x):
        print(x)
        m=1
if m==0:
    print('none')
    
