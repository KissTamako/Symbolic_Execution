#!/usr/bin/env python
"""
修复 wrap_concrete_constant 函数和 Z3 表达式转换问题
"""
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

# 首先备份原始文件
import shutil

def backup_file(filepath):
    if os.path.exists(filepath):
        backup_path = filepath + '.bak'
        shutil.copy2(filepath, backup_path)
        print(f"已备份: {filepath} -> {backup_path}")
        return True
    return False

print("=== 开始修复 wrap_concrete_constant 和 Z3 表达式转换 ===")

# 1. 修复 runtime_helpers.py 中的 wrap_concrete_constant 函数
print("\n1. 修复 runtime_helpers.py...")
runtime_helpers_path = 'symbolic/runtime_helpers.py'
backup_file(runtime_helpers_path)

# 读取原始内容
with open(runtime_helpers_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找 wrap_concrete_constant 函数
import re

# 找到 wrap_concrete_constant 函数定义
pattern = r'(def wrap_concrete_constant\(value\):\s*\n\s*""".*?"""\s*\n\s*from .symbolic_types\.symbolic_int import SymbolicInteger\s*\n\s*from .symbolic_types\.symbolic_str import SymbolicStr\s*\n\s*.*?\n\s*if isinstance\(value, bool\):\s*\n\s*#.*?\n\s*return value\s*\n\s*elif isinstance\(value, int\):\s*\n\s*)return SymbolicInteger\("const", value, None\)'

match = re.search(pattern, content, re.DOTALL)
if match:
    print("   找到 wrap_concrete_constant 函数定义")
    # 修改整数常量的包装
    new_content = re.sub(
        r'return SymbolicInteger\("const", value, None\)',
        r'return SymbolicInteger("const", value, None)',
        content
    )
    
    # 实际上我们需要修复的不是这里，而是检查 SymbolicInteger 的实现
    # 让我们检查 SymbolicInteger 是否正确实现了 isVariable 方法
    print("   检查 SymbolicInteger 实现...")
    
    # 写入修复后的内容
    with open(runtime_helpers_path, 'w', encoding='utf-8') as f:
        f.write(content)  # 暂时不修改，先检查其他问题
    print("   保持原样，先检查其他问题")
else:
    print("   未找到 wrap_concrete_constant 函数定义，可能格式不同")

# 2. 检查 Z3 表达式转换问题
print("\n2. 检查 Z3 表达式转换...")
z3_expr_path = 'symbolic/z3_expr/expression.py'
backup_file(z3_expr_path)

with open(z3_expr_path, 'r', encoding='utf-8') as f:
    z3_content = f.read()

# 检查 _astToZ3Expr 方法中处理 SymbolicInteger 的部分
print("   检查 _astToZ3Expr 方法...")

# 查找处理 SymbolicInteger 的代码段
symbolic_integer_pattern = r'elif isinstance\(expr, SymbolicInteger\):\s*\n\s*if expr\.isVariable\(\):\s*\n\s*if env == None:\s*\n\s*# Handle \'const\' variable specially - it\'s not a real variable\s*\n\s*if expr\.name == \'const\':\s*\n\s*# \'const\' is a placeholder for concrete constants\s*\n\s*# Return concrete value as Z3 constant\s*\n\s*concrete_val = expr\.getConcrValue\(\) if hasattr\(expr, \'getConcrValue\'\) else int\(expr\)\s*\n\s*return IntVal\(concrete_val\)'

if re.search(symbolic_integer_pattern, z3_content, re.DOTALL):
    print("   找到 SymbolicInteger 处理代码")
    
    # 问题可能是 IntVal 没有正确导入或者使用方式不对
    # 检查文件开头的导入
    if 'from z3 import *' in z3_content:
        print("   ✓ 已导入 z3 模块")
    else:
        print("   ✗ 未找到 z3 导入")
    
    # 检查 IntVal 是否可用
    print("   检查 IntVal 函数...")
    
    # 让我们修复可能的问题：确保 IntVal 正确使用
    # 查找并修复 IntVal 调用
    new_z3_content = z3_content
    
    # 修复点1: 确保 IntVal 有正确的参数
    # IntVal(v, solver.ctx) 而不是 IntVal(v)
    # 但在 integer.py 中我们看到 _constant 方法使用 IntVal(v, solver.ctx)
    
    # 问题可能在于：当 expr.name == 'const' 时，应该调用 _constant 方法而不是直接使用 IntVal
    # 让我们修改这部分代码
    fix_pattern = r'(\s*if expr\.name == \'const\':\s*\n\s*# \'const\' is a placeholder for concrete constants\s*\n\s*# Return concrete value as Z3 constant\s*\n\s*)concrete_val = expr\.getConcrValue\(\) if hasattr\(expr, \'getConcrValue\'\) else int\(expr\)\s*\n\s*return IntVal\(concrete_val\)'
    
    def replace_func(match):
        prefix = match.group(1)
        return prefix + 'concrete_val = expr.getConcrValue() if hasattr(expr, \'getConcrValue\') else int(expr)\n\t\t\t\treturn self._constant(concrete_val, solver)'
    
    new_z3_content = re.sub(fix_pattern, replace_func, new_z3_content)
    
    # 同样修复 env != None 的情况
    fix_pattern2 = r'(\s*if expr\.name == \'const\':\s*\n\s*# \'const\' is a placeholder for concrete constants\s*\n\s*# Return concrete value as Python int\s*\n\s*)concrete_val = expr\.getConcrValue\(\) if hasattr\(expr, \'getConcrValue\'\) else int\(expr\)\s*\n\s*return concrete_val'
    
    def replace_func2(match):
        prefix = match.group(1)
        return prefix + 'concrete_val = expr.getConcrValue() if hasattr(expr, \'getConcrValue\') else int(expr)\n\t\t\t\treturn concrete_val'
    
    new_z3_content = re.sub(fix_pattern2, replace_func2, new_z3_content, flags=re.DOTALL)
    
    # 写入修复后的内容
    if new_z3_content != z3_content:
        with open(z3_expr_path, 'w', encoding='utf-8') as f:
            f.write(new_z3_content)
        print("   已修复 Z3 表达式转换中的 IntVal 调用")
    else:
        print("   无需修改 Z3 表达式转换")
else:
    print("   未找到 SymbolicInteger 处理代码，可能结构不同")

print("\n3. 创建测试验证修复...")
test_code = '''
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

print("测试修复结果...")

try:
    from symbolic.runtime_helpers import wrap_concrete_constant
    from symbolic.z3_expr.expression import Z3Expression
    from symbolic.z3_expr.integer import Z3Integer
    import z3
    
    # 测试 wrap_concrete_constant
    wrapped = wrap_concrete_constant(5)
    print(f"wrap_concrete_constant(5) = {wrapped}")
    print(f"类型: {type(wrapped)}")
    print(f"name: {wrapped.name if hasattr(wrapped, 'name') else '无name属性'}")
    print(f"isVariable(): {wrapped.isVariable() if hasattr(wrapped, 'isVariable') else '无isVariable方法'}")
    print(f"expr: {wrapped.expr if hasattr(wrapped, 'expr') else '无expr属性'}")
    
    # 测试 Z3 转换
    solver = z3.Solver()
    z3_expr = Z3Integer()  # 使用 Z3Integer 而不是 Z3Expression
    
    # 测试 _constant 方法
    const_expr = z3_expr._constant(5, solver)
    print(f"_constant(5, solver) = {const_expr}, 类型: {type(const_expr)}")
    
    # 测试处理 SymbolicInteger
    print("\\n测试 SymbolicInteger 转换...")
    result = z3_expr._astToZ3Expr(wrapped, solver, None)
    print(f"_astToZ3Expr(wrapped, solver, None) = {result}, 类型: {type(result)}")
    
    # 测试简单表达式
    print("\\n测试简单表达式转换...")
    # 创建表达式: x + 1
    # 首先需要创建变量 'x'
    x_var = z3_expr._getIntegerVariable('x', solver)
    print(f"变量 x: {x_var}")
    
    # 创建表达式 ['+', 'x', wrapped]
    expr = ['+', 'x', wrapped]
    result2 = z3_expr._astToZ3Expr(expr, solver, {'x': x_var})
    print(f"表达式 {expr} 转换结果: {result2}, 类型: {type(result2)}")
    
except Exception as e:
    print(f"测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
'''

test_file = 'test_fix_validation.py'
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(test_code)

print(f"   已创建测试文件: {test_file}")
print("   运行命令: python test_fix_validation.py")

print("\n=== 修复完成 ===")
print("下一步: 运行测试验证修复效果")