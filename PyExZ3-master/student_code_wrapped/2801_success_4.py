from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def check_number(pass_word):
    for i in pass_word:
        if i.isdigit():
            return True
    return False
def check_upperletter(pass_word):
    for i in pass_word:
        if i.isalpha():
            if i.isupper():
                return True
    return False
def check_lowerletter(pass_word):
    for i in pass_word:
        if i.isalpha():
            if i.islower():
                return True
    return False
def check_punct(pass_word):
    for i in pass_word:
        if i.isdigit()==False:
            if i.isalpha()==False:
                return True
    return False

a = input('请输入密码：')
i = 0
if len(a)>=8:
    i+=1
if check_number(a):
    i+=1
if check_upperletter(a):
    i+=1
if check_lowerletter(a):
    i+=1
if check_punct(a):
    i+=1
print(i)
