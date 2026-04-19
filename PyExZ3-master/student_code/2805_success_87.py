def main():
    a = input()
    print(strreduce(a))

def strreduce(a):
    a=list(a)
    b=[]
    for i in a:
        if i not in b:
            b.append(i)
    s=("".join(map(str,b)))
    return(s)

    


main()

