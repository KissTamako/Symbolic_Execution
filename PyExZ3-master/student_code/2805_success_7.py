def main():
    a = input()
    print(strreduce(a))

def strreduce(n):
    s=''
    for x in n:
        if x not in s:
            s+=x
    return s

main()

