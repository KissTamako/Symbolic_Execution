from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def job(time):  
#time存放三个人完成三个任务的时间。time的结构是二维列表。
#可以用穷举求解。可以用set判断某种调度方案是否有重复人员，例如“AAB”
#函数有两个返回值，一个是最优方案的时间，一个是执行顺序(字符串)
    a2=['A','B','C']
    a=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,1,0],[2,0,1]]
    b=[]
    for i in a:
        d=[]
        for j in range(3):
            c=time[i[j]][j]
            d.append(c)
        b.append(sum(d))
    b1=sorted(b)
    e=b1[0]
    index1=b.index(e)
    a1=a[index1]
    a3=''
    for k in a1:
         a3+=a2[k]
    l=[e,a3]
    return l


time_all=[]
for x in range(3):#读3行        
      time_one=input().split()
      time_one=[eval(x) for x in time_one]
      time_all.append(time_one)
result=job(time_all)
for x in result:
    print(x,end=" ")

