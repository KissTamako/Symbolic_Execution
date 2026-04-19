from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def myFun(para2):
       if  not para2[0::]:  #递归结束条件
              print("#",end="")       
       else:
              myFun(para2[1:])        
              print(para2[0] ,end="")      


para1=input()
myFun(para1) #调用自定义函数

