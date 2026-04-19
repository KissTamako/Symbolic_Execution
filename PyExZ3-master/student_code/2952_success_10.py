def print_matrix(n):
        matrix=[]
        for i in range(n):
            row=[]
            for j in range(n):
                row.append(min(i,j)+1)
            matrix.append(row)
            print(*matrix[i])

number=eval(input())
print_matrix(number)



