def main():
    N,M = map(int,input().split())
    calculate_capital(N,M)
    print('%.4f'%calculate_capital(N,M))
def calculate_capital(N,M):
        a=N*(1.003**M)
        return a

main()



