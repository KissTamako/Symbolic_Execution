def matrix(n=2): 
    ls=[['*']*n]*n
    for x in range(n):
        for y in range(n):
            if n==2:
                print(ls[x][y],end='\n' if y==1 else ' ')
            else:
                print(ls[x][y],end='\n' if y==n-1 else ' ')


number=input()
if number=="default":
    matrix() #无实参调用自定义函数
else:
    matrix(eval(number))  #有实参调用自定义函数

