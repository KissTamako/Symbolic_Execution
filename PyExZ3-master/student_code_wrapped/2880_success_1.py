from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def level(mylist):
    max_level=0
    level_list=[]
  # 递归函数的头部
    if isinstance(mylist,list): #判断mylist变量是否是一个列表
        for x in mylist:
                                level_list.append(level(x))
                                max_level=max(level_list)
          #求列表的每一个元素的嵌套层数的最大值

  #求列表的每一个元素的嵌套层数的最大值
        return max_level+1
    else: #不是列表，递归结束条件
        return 0

origin=eval(input())
print(level(origin))

