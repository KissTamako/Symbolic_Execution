def merge(array1,array2):#&#160;该函数用来将两个有序序列合并成一个有序序列
    array3=[]  #合并的列表
    p1=p2=0  #两个搜索位置，一个搜索 array1, 一个搜索array2
    while p1<len(array1) and p2<len(array2):  #两个列表都没有搜索完
        if array1[p1]<array2[p2]:   #p1位置的array1元素比p2位置的array2元素小
            array3.append(array1[p1])  
            p1+=1  # 搜索array1的下一个元素
        else:  
            array3.append(array2[p2])
            p2+=1
    if p1==len(array1):  #array1先搜索完
        array3=array3+array2[p2:]   #处理array2剩余的部分
    else:   #array2先搜索完
        array3=array3+array1[p1:]
    return array3
    
def mysort(mylist): #该函数实现递归的归并排序
    if len(mylist)<=1:  # 递归结束条件
        return mylist
    middle=len(mylist)//2        
    left_list,right_list=mysort(mylist[:middle]),mysort(mylist[middle:])       #对列表的左半部分和右半部分分别做归并排序
    return merge(left_list,right_list)

origin=input().split()
for x in range(len(origin)):
     origin[x]=int(origin[x])
result=mysort(origin)
for x in result:
     print(x,end=" ")

