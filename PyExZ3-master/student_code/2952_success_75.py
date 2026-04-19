def print_matrix(n):
    for i in range(n):
            row = []
            for j in range(n):
                row.append(min(i,j)+1)
            print(*row)


number=eval(input())
print_matrix(number)



