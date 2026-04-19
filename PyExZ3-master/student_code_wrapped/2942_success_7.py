from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

a = input()
b = input()
la = len(a)
lb = len(b)
#建立二维列表，行数la+1，列数lb+1,初值为0
res = [[0 for i in range(lb+1)] for j in range(la+1)]
lc = []
mmax = 0
for i in range(1, la+1):
   for j in range(1, lb+1):
      if a[i-1] == b[j-1]:
         res[i][j] = res[i-1][j-1] + 1
         if(res[i][j]>mmax):
            mmax = res[i][j]

print(mmax)


