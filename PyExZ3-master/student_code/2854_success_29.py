def insert(num,array1): #把整数num插入非递减顺序列表array1，插入后仍然保持非递减顺序不变
    place=0  
    for x in array1:
          if num<x:  #找到array1里面第一个比num大的数
              break
          else:
              place+=1  #更新place
    return array1[:place] +[num]+array1[place:]  #num插入array1的place位置
    
def mysort(array2):  #该函数实现递归的插入排序
    temp=[]
    if len(array2)==1: #递归结束条件
        return array2
    else:
        while len(array2)>1:
                        temp.append(min(array2))
                        array2.remove(min(array2))     #对除去最后一个元素的列表进行插入排序
        temp=insert(array2[-1],temp) #把最后一个数插入到前面排好序的列表里
        return temp
       
origin=input().split()
for x in range(len(origin)):
    origin[x]=eval(origin[x])
result=mysort(origin)
for x in result:
    print(x,end=" ")

      
        

