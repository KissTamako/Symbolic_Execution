from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

x = input()
y = input()
def anagramSolution(s1,s2):
    if len(s1)!=len(s2):
        return False
    list_1=list(s1)
    n=len(s1) 
    for c in s2:
        found = False 
        for i in range(n): 
            if list_1[i]==c:
                return True 
            list_1[i]=None 
            break
        if not found: 
            return False
    return True
print(anagramSolution(x,y)) 
