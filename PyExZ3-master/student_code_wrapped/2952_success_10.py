from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

def print_matrix(n):
        matrix=[]
        for i in range(n):
            row=[]
            for j in range(n):
                row.append(min(i,j)+1)
            matrix.append(row)
            print(*matrix[i])

number=eval(input())
print_matrix(number)



