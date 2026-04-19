def  myFun(a,b):
       n=0
       b=int(b)
       for i in range(len(a)):
           a=int(a)
           n=n+(a%10)*(b%10)
           a=a//10
           b=b//10
       return n

num=input().split()
a=num[0]
b=num[1]
if a.isdigit() and b.isdigit(): #判断a,b是否都是数字
       print(myFun(a,b))  #调用自定义函数
else:
       print("error")

