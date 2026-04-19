def test(*para):
        a=1
        if para=='0':
             return -1
        if para!='0':
            for i in para:
                 a*=int(i)
            if a ==1:
                 return -1
            else:
                 return a
    

origin=input().split()
origin=[eval(x) for x in origin]
number=origin[0]  #获取参数个数
if number==0:
    result=test()
elif number==1:
    result=test(origin[1])
elif number==2:
    result=test(origin[1],origin[2])
elif number==3:
    result=test(origin[1],origin[2],origin[3])
print(result)

