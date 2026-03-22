#!/usr/bin/env python3
"""测试loader中的常量提升功能"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# 创建一个测试文件
test_file_content = '''
from symbolic.symbolic_types.symbolic_int import SymbolicInteger

def test_function():
    x = SymbolicInteger("x", 3)
    
    # 测试常量方法调用
    # 如果常量提升生效，这应该返回SymbolicInteger而不是int
    result = (5).__add__(x)
    print(f"(5).__add__(x) = {result}, type: {type(result)}")
    
    # 检查是否是符号类型
    if hasattr(result, 'getConcrValue'):
        print(f"✓ 常量提升生效！结果是SymbolicInteger，具体值: {result.getConcrValue()}")
        return True
    else:
        print(f"✗ 常量提升未生效！结果是普通int: {result}")
        return False
'''

# 写入测试文件
test_filename = "test_upcast_integration.py"
with open(test_filename, 'w', encoding='utf-8') as f:
    f.write(test_file_content)

print(f"创建测试文件: {test_filename}")
print("测试文件内容:")
print(test_file_content)

# 测试AST转换器
print("\n" + "="*60)
print("测试AST转换器单独工作:")
from symbolic.ast_upcaster import transform_source_code

# 测试转换
test_source = '(5).__add__(x)'
transformed, code_obj = transform_source_code(test_source)
print(f"原始: {test_source}")
print(f"转换: {transformed}")
print(f"是否包含SymbolicInteger: {'SymbolicInteger' in (transformed or '')}")

# 测试完整函数转换
print("\n" + "="*60)
print("测试完整函数转换:")
func_source = '''def test():
    x = SymbolicInteger("x", 3)
    return (5).__add__(x)'''

transformed_func, _ = transform_source_code(func_source)
print(f"原始函数:\n{func_source}")
print(f"转换后:\n{transformed_func}")

# 测试通过loader加载
print("\n" + "="*60)
print("测试通过loader加载:")

try:
    from symbolic.loader import loaderFactory
    
    # 创建loader
    loader = loaderFactory(test_filename, "test_function")
    if loader:
        print("✓ loader创建成功")
        
        # 创建调用
        inv = loader.createInvocation()
        
        # 执行
        print("执行测试函数...")
        result = inv.callFunction({})
        
        if result:
            print("✓ 测试通过")
        else:
            print("✗ 测试失败")
    else:
        print("✗ loader创建失败")
        
except Exception as e:
    print(f"✗ loader测试出错: {e}")
    import traceback
    traceback.print_exc()

# 清理
if os.path.exists(test_filename):
    os.remove(test_filename)
    print(f"\n清理测试文件: {test_filename}")

print("\n测试完成")