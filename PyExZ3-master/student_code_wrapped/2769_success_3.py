from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

Uplist=['A', 'B', 'C', 'D', 'E', \
'F', 'G', 'H', 'I', 'J', 'K', 'L',\
'M', 'N', 'O', 'P', 'Q', 'R', 'S',\
'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Lowlist=['a', 'b', 'c', 'd', 'e',\
'f', 'g', 'h', 'i', 'j', 'k', 'l',\
'm', 'n', 'o', 'p', 'q', 'r', 's',\
't', 'u', 'v', 'w', 'x', 'y', 'z']
a=list(input())
b=a[:]
print("".join(str(i) for i in a))
for x in b:
    if x in Uplist:
        m = Uplist.index(str(x))
        print(Uplist[25-m],end="")
    elif x in Lowlist:
        n = Lowlist.index(str(x))
        print(Lowlist[25-n],end="")
    else:
        pass
        print(x,end="")