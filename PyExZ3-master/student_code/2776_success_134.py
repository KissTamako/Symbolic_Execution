def  myFun(a,b):
           sum=0
           maxlen=max(len(a),len(b))
           a=a.rjust(maxlen,'0')
           b=b.rjust(maxlen,'0')
           for i in range(maxlen):
                   sum+=int(a[i])*int(b[i])
           return sum

num=input().split()
a=num[0]
b=num[1]
if a.isdigit() and b.isdigit(): #判断a,b是否都是数字
       print(myFun(a,b))  #调用自定义函数
else:
       print("error")

