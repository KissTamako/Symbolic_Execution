def main():
    num = eval(input())
    calculate_e(num)
    print('%.6f'%calculate_e(num))
def calculate_e(num):
    a=1
    for i in range(1,num+1):
        b=i
        for j in range(1,i):
            b*=j
        a=a+1/b
    return a

main()


