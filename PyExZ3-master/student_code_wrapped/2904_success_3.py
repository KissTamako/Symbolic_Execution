from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

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

