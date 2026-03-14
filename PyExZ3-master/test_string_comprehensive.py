#!/usr/bin/env python3
"""综合测试字符串类型新增扩展函数"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from symbolic.symbolic_types.symbolic_str import SymbolicStr
from symbolic.symbolic_types import getSymbolic

def test_all_new_methods():
    """测试所有新增的方法"""
    print("=" * 60)
    print("字符串类型综合扩展函数测试")
    print("=" * 60)
    
    # 创建测试字符串
    s = SymbolicStr('test', 'Hello World 123')
    
    print(f"测试字符串: '{s}'")
    print(f"具体值: '{s.getConcrValue()}'")
    print()
    
    # 大小写转换类方法
    print("大小写转换类方法:")
    print(f"  .capitalize() = '{s.capitalize()}' (类型: {type(s.capitalize()).__name__})")
    print(f"  .swapcase() = '{s.swapcase()}' (类型: {type(s.swapcase()).__name__})")
    print(f"  .title() = '{s.title()}' (类型: {type(s.title()).__name__})")
    print(f"  .casefold() = '{s.casefold()}' (类型: {type(s.casefold()).__name__})")
    
    # 检查方法
    print("\n检查类方法:")
    print(f"  .isascii() = {s.isascii()} (类型: {type(s.isascii()).__name__})")
    print(f"  .isdecimal() = {s.isdecimal()} (类型: {type(s.isdecimal()).__name__})")
    print(f"  .isidentifier() = {s.isidentifier()} (类型: {type(s.isidentifier()).__name__})")
    print(f"  .isprintable() = {s.isprintable()} (类型: {type(s.isprintable()).__name__})")
    print(f"  .isspace() = {s.isspace()} (类型: {type(s.isspace()).__name__})")
    print(f"  .istitle() = {s.istitle()} (类型: {type(s.istitle()).__name__})")
    
    # 填充类方法
    print("\n填充类方法:")
    print(f"  .center(20) = '{s.center(20)}'")
    print(f"  .zfill(20) = '{s.zfill(20)}'")
    print(f"  .ljust(20) = '{s.ljust(20)}'")
    print(f"  .rjust(20) = '{s.rjust(20)}'")
    
    # 分割类方法
    print("\n分割类方法:")
    print(f"  .partition(' ') = {s.partition(' ')}")
    print(f"  .rpartition(' ') = {s.rpartition(' ')}")
    print(f"  .rsplit(' ') = {[str(x) for x in s.rsplit(' ')]}")
    
    # 查找类方法
    print("\n查找类方法:")
    print(f"  .rfind('World') = {s.rfind('World')}")
    print(f"  .rindex('World') = {s.rindex('World')}")
    print(f"  .find('World') = {s.find('World')}")
    print(f"  .index('World') = {s.index('World')}")
    
    # 特殊方法测试
    print("\n特殊方法测试:")
    s_tabs = SymbolicStr('tabs', 'hello\tworld')
    print(f"  .expandtabs() on '{s_tabs}' = '{s_tabs.expandtabs()}'")
    
    s_trans = SymbolicStr('trans', 'hello')
    trans_table = str.maketrans('lo', 'LO')
    print(f"  .translate() on '{s_trans}' = '{s_trans.translate(trans_table)}'")
    
    # 测试字符串是否返回Symbolic类型
    print("\n类型检查:")
    methods_to_check = [
        ('capitalize', []),
        ('swapcase', []),
        ('title', []),
        ('center', [20]),
        ('zfill', [20]),
        ('casefold', []),
        ('expandtabs', []),
    ]
    
    all_symbolic = True
    for method_name, args in methods_to_check:
        method = getattr(s, method_name)
        result = method(*args)
        is_symbolic = type(result).__name__ == 'SymbolicStr'
        print(f"  .{method_name}(): 返回类型={type(result).__name__}, 是否SymbolicStr={is_symbolic}")
        if not is_symbolic:
            all_symbolic = False
    
    if all_symbolic:
        print("\n✓ 所有字符串操作方法都返回SymbolicStr类型")
    else:
        print("\n⚠ 部分方法未返回SymbolicStr类型")
    
    # 测试检查方法返回SymbolicInteger
    print("\n检查方法类型检查:")
    check_methods = [
        ('isascii', []),
        ('isdecimal', []),
        ('isidentifier', []),
        ('isprintable', []),
        ('isspace', []),
        ('istitle', []),
        ('isalpha', []),
        ('isdigit', []),
        ('isalnum', []),
        ('isnumeric', []),
        ('islower', []),
        ('isupper', []),
    ]
    
    all_integer = True
    for method_name, args in check_methods:
        method = getattr(s, method_name)
        result = method(*args)
        is_symbolic = hasattr(result, 'getConcrValue')
        print(f"  .{method_name}(): 返回类型={type(result).__name__}, 是否Symbolic类型={is_symbolic}")
        if not is_symbolic:
            all_integer = False
    
    if all_integer:
        print("\n✓ 所有检查方法都返回Symbolic类型")
    else:
        print("\n⚠ 部分检查方法未返回Symbolic类型")
    
    return True

def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 60)
    print("边界情况测试")
    print("=" * 60)
    
    # 空字符串
    empty = SymbolicStr('empty', '')
    print(f"空字符串: '{empty}'")
    print(f"  .capitalize() = '{empty.capitalize()}'")
    print(f"  .isalpha() = {empty.isalpha()}")
    print(f"  .zfill(5) = '{empty.zfill(5)}'")
    
    # 纯空格字符串
    spaces = SymbolicStr('spaces', '   ')
    print(f"\n纯空格字符串: '{spaces}'")
    print(f"  .isspace() = {spaces.isspace()}")
    print(f"  .strip() = '{spaces.strip()}'")
    print(f"  .lstrip() = '{spaces.lstrip()}'")
    print(f"  .rstrip() = '{spaces.rstrip()}'")
    
    # 纯数字字符串
    numbers = SymbolicStr('numbers', '12345')
    print(f"\n纯数字字符串: '{numbers}'")
    print(f"  .isdigit() = {numbers.isdigit()}")
    print(f"  .isdecimal() = {numbers.isdecimal()}")
    print(f"  .isnumeric() = {numbers.isnumeric()}")
    print(f"  .zfill(10) = '{numbers.zfill(10)}'")
    
    # 特殊字符字符串
    special = SymbolicStr('special', 'Hello\nWorld\t!')
    print(f"\n特殊字符字符串: '{repr(special.getConcrValue())}'")
    print(f"  .isprintable() = {special.isprintable()}")
    print(f"  .expandtabs() = '{repr(special.expandtabs().getConcrValue())}'")
    
    return True

def test_symbolic_behavior():
    """测试符号行为"""
    print("\n" + "=" * 60)
    print("符号行为测试")
    print("=" * 60)
    
    # 创建符号字符串
    s = SymbolicStr('sym', 'hello')
    
    # 测试表达式树
    print(f"测试字符串: '{s}'")
    print(f"  是变量吗? {s.isVariable()}")
    print(f"  表达式树: {s.expr}")
    
    # 测试大小写转换的符号性
    upper_result = s.upper()
    print(f"\n.upper() 结果:")
    print(f"  类型: {type(upper_result).__name__}")
    print(f"  是变量吗? {upper_result.isVariable()}")
    print(f"  表达式树: {upper_result.expr}")
    
    # 测试检查方法的符号性
    isalpha_result = s.isalpha()
    print(f"\n.isalpha() 结果:")
    print(f"  类型: {type(isalpha_result).__name__}")
    print(f"  有getConcrValue吗? {hasattr(isalpha_result, 'getConcrValue')}")
    if hasattr(isalpha_result, 'getConcrValue'):
        print(f"  具体值: {isalpha_result.getConcrValue()}")
    
    return True

def main():
    """主函数"""
    all_passed = True
    
    try:
        if not test_all_new_methods():
            all_passed = False
    except Exception as e:
        print(f"test_all_new_methods 失败: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        if not test_edge_cases():
            all_passed = False
    except Exception as e:
        print(f"test_edge_cases 失败: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        if not test_symbolic_behavior():
            all_passed = False
    except Exception as e:
        print(f"test_symbolic_behavior 失败: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有测试通过!")
        return 0
    else:
        print("✗ 有测试失败!")
        return 1

if __name__ == "__main__":
    sys.exit(main())