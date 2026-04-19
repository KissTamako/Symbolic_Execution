def matrix(n=2): 
    if n==2:
        for i in range(2):
            print('* *') 
    else:
        s='* '
        s1=s*int(number)
        s2=str(s1[0:-1])
        for i in range(int(number)):
            print(s2)

number=input()
if number=="default":
    matrix() #无实参调用自定义函数
else:
    matrix(int(number))  #有实参调用自定义函数

