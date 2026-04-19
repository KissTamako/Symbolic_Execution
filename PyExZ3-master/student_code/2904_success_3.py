def main():
    a=int(input())
    calculate_sum(a)
def calculate_sum(a):
    c=1
    k=0
    s=0
    d=a
    if a<10:
        for y in range(a):
            s+=a*10**y
            k+=s
    else:
        while True:
            if a //10==0:
                break
            c+=1
            a//=10
        for y in range(0,c*d,c):
            s+=d*10**y
            k+=s

    print(k)
main()

