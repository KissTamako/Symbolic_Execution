#!/usr/bin/env python3
"""简单测试常量提升功能"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# 1. 首先测试AST转换器本身
print("="*60)
print("测试AST转换器")
print("="*60)

from symbolic.ast_upcaster import transform_source_code

# 测试简单表达式
test_code = '(5).__add__(x)'
transformed, code_obj = transform_source_code(test_code)
print(f"原始代码: {test_code}")
print(f"转换后: {transformed}")
print(f"转换成功: {'SymbolicInteger' in (transformed or '')}")

# 2. 测试完整函数
print("\n" + "="*60)
print("测试完整函数转换")
print("="*60)

func_code = '''def my_test():
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    x = SymbolicInteger("x", 3)
    return (5).__add__(x)'''

transformed_func, code_obj = transform_source_code(func_code)
print(f"原始函数:\n{func_code}")
print(f"\n转换后:\n{transformed_func}")

# 3. 执行转换后的代码
print("\n" + "="*60)
print("执行转换后的代码")
print("="*60)

# 创建一个模块来执行转换后的代码
module_globals = {}
try:
    exec(code_obj, module_globals)
    
    # 调用函数
    if 'my_test' in module_globals:
        result = module_globals['my_test']()
        print(f"函数执行结果: {result}")
        print(f"结果类型: {type(result)}")
        
        if hasattr(result, 'getConcrValue'):
            print(f"✓ 常量提升生效！结果是SymbolicInteger")
            print(f"  具体值: {result.getConcrValue()}")
        else:
            print(f"✗ 常量提升未生效！结果是普通{type(result).__name__}")
    else:
        print("✗ 函数未定义")
        
except Exception as e:
    print(f"✗ 执行出错: {e}")
    import traceback
    traceback.print_exc()

# 4. 测试其他类型的常量提升
print("\n" + "="*60)
print("测试其他类型常量提升")
print("="*60)

test_cases = [
    ('"abc".__contains__("b")', '字符串包含'),
    ('"hello".upper()', '字符串大写'),
    ('3.14.__add__(2.0)', '浮点数加法'),
]

for code, desc in test_cases:
    transformed, _ = transform_source_code(code)
    print(f"\n{desc}:")
    print(f"  原始: {code}")
    print(f"  转换: {transformed[:80] if transformed else '<无输出>'}")
    
    if transformed and ('SymbolicStr' in transformed or 'SymbolicFloat' in transformed):
        print(f"  ✓ 转换成功")
    else:
        print(f"  ✗ 转换失败或未转换")

print("\n" + "="*60)
print("测试完成")
print("="*60)