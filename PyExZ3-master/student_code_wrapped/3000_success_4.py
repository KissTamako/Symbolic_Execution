from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

# fruits = ['grape','pear','apple','water melon']
# fruits.reverse()
# print("reversed fruits:",fruits)

# fruits = ['grape','pear','apple','water melon']
# fruits.sort(key=len)
# print("sorted fruits by len:",fruits)

# v = [7,11,13]
# print(max(v))
# print(min(v))
# print(sum(v))
# print("%.2f" %(sum(v)/len(v)))

# suits = ['红','梅','黑','方']
# ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
# cards = [suit + rank for suit in suits for rank in ranks]
# print(cards)

# print(list(range(0,4)))
# print(list(range(7,11)))
# print(list(range(1,14,3)))
# print(list(range(15,2,-4)))
# print(list(range(-20,20,6)))
# print(list(range(-1,-22,-7)))

# v1 = [x for x in range(-5,10,2)]
# v2 = "".join([chr(ord('a')+x) for x in range(26)])
# print("v1:",v1)
# print("v2:",v2)
# print(v1[:5])   #期望输出：[-5, -3, -1, 1, 3]
# print(v1[-6:-1])   #期望输出：[-1, 1, 3, 5, 7]
# print(v1[-1:1:-2])   #期望输出：[9, 5, 1]
# print(v2[:])   #期望输出：abcdefghijklmnopqrstuvwxyz
# print(v2[::-5])   #期望输出：zupkfa
# print(v2[::-1])   #期望输出：zyxwvutsrqponmlkjihgfedcba
# print(v2[:-5:7])   #期望输出：aho

# a = [1,2,3,4,5,6,7]
# b = a
# c = a[:]
# a[3:5] = 99,100
# print("a=",a,id(a)==id(b))
# print("b=",b)
# print("c=",c,id(c)==id(a))

lst=eval(input())
print('%.2f'%(sum(lst)/len(lst)))
