id_ls=list(input())
if len(id_ls) != 18:
    print("Error")
else:
    pass
    num_sum=0
    num=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    for x in range(17):
        num_sum += int(id_ls[x])*num[x]
    num_exam = num_sum % 11
    exam_dict={0:"1",1:"0",2:"X",3:"9",4:"8",5:"7",6:"6",7:"5",8:"4",9:"3",10:"2"}
    if exam_dict[num_exam] == id_ls[17]:
        print("Correct")
    else:
        print("Wrong")
    