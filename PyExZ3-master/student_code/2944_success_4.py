def  stuid(data2):
        a=[]
        for i in data2:
            a.append(i[0:8])
        return a

data1=input().split()
student_id=stuid(data1)
for x in student_id:
    print(x,end=" ")


        

