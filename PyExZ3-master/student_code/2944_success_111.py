def  stuid(data2):
    data3=[]
    for x in data2:
        data3.append(x[:8])
    return data3


data1=input().split()
student_id=stuid(data1)
for x in student_id:
    print(x,end=" ")


        

