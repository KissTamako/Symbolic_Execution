def  stuid(data2):
    lst=[]
    for i in data2:
        lst.append(i[0:8])
    return lst

data1=input().split()
student_id=stuid(data1)
for x in student_id:
    print(x,end=" ")


        

