def myFun(para2):
       if para2=='':
  #递归结束条件
              print("#",end="")       
       else:
              myFun(para2[1:])        
              print(para2[0],end='')    


para1=input()
myFun(para1) #调用自定义函数

