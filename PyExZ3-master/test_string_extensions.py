#!/usr/bin/env python3
"""测试字符串类型新增扩展函数"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from symbolic.symbolic_types.symbolic_str import SymbolicStr
from symbolic.symbolic_types import getSymbolic

def test_capitalize():
    """测试capitalize函数"""
    print("测试 capitalize 函数:")
    
    # 创建符号字符串
    s1 = SymbolicStr('s1', 'hello world')
    s2 = SymbolicStr('s2', 'HELLO')
    s3 = SymbolicStr('s3', '123abc')
    
    # 测试capitalize
    result1 = s1.capitalize()
    result2 = s2.capitalize()
    result3 = s3.capitalize()
    
    print(f"  '{s1}'.capitalize() = '{result1}'")
    print(f"  '{s2}'.capitalize() = '{result2}'")
    print(f"  '{s3}'.capitalize() = '{result3}'")
    
    # 检查具体值
    concr1 = result1.getConcrValue() if hasattr(result1, 'getConcrValue') else result1
    concr2 = result2.getConcrValue() if hasattr(result2, 'getConcrValue') else result2
    concr3 = result3.getConcrValue() if hasattr(result3, 'getConcrValue') else result3
    
    expected1 = 'Hello world'
    expected2 = 'Hello'
    expected3 = '123abc'
    
    print(f"  具体值检查: '{concr1}' (期望: '{expected1}')")
    print(f"  具体值检查: '{concr2}' (期望: '{expected2}')")
    print(f"  具体值检查: '{concr3}' (期望: '{expected3}')")
    
    return True

def test_swapcase():
    """测试swapcase函数"""
    print("\n测试 swapcase 函数:")
    
    s1 = SymbolicStr('s1', 'Hello World')
    s2 = SymbolicStr('s2', 'HELLO')
    s3 = SymbolicStr('s3', 'hello')
    s4 = SymbolicStr('s4', '123')
    
    result1 = s1.swapcase()
    result2 = s2.swapcase()
    result3 = s3.swapcase()
    result4 = s4.swapcase()
    
    print(f"  '{s1}'.swapcase() = '{result1}'")
    print(f"  '{s2}'.swapcase() = '{result2}'")
    print(f"  '{s3}'.swapcase() = '{result3}'")
    print(f"  '{s4}'.swapcase() = '{result4}'")
    
    return True

def test_title():
    """测试title函数"""
    print("\n测试 title 函数:")
    
    s1 = SymbolicStr('s1', 'hello world')
    s2 = SymbolicStr('s2', 'HELLO WORLD')
    s3 = SymbolicStr('s3', "it's a test")
    
    result1 = s1.title()
    result2 = s2.title()
    result3 = s3.title()
    
    print(f"  '{s1}'.title() = '{result1}'")
    print(f"  '{s2}'.title() = '{result2}'")
    print(f"  '{s3}'.title() = '{result3}'")
    
    return True

def test_center():
    """测试center函数"""
    print("\n测试 center 函数:")
    
    s1 = SymbolicStr('s1', 'hello')
    
    result1 = s1.center(10)
    result2 = s1.center(10, '*')
    result3 = s1.center(3)
    
    print(f"  '{s1}'.center(10) = '{result1}'")
    print(f"  '{s1}'.center(10, '*') = '{result2}'")
    print(f"  '{s1}'.center(3) = '{result3}'")
    
    return True

def test_zfill():
    """测试zfill函数"""
    print("\n测试 zfill 函数:")
    
    s1 = SymbolicStr('s1', '42')
    s2 = SymbolicStr('s2', '-42')
    s3 = SymbolicStr('s3', '+42')
    s4 = SymbolicStr('s4', 'hello')
    
    result1 = s1.zfill(5)
    result2 = s2.zfill(5)
    result3 = s3.zfill(5)
    result4 = s4.zfill(5)
    
    print(f"  '{s1}'.zfill(5) = '{result1}'")
    print(f"  '{s2}'.zfill(5) = '{result2}'")
    print(f"  '{s3}'.zfill(5) = '{result3}'")
    print(f"  '{s4}'.zfill(5) = '{result4}'")
    
    return True

def test_partition():
    """测试partition函数"""
    print("\n测试 partition 函数:")
    
    s1 = SymbolicStr('s1', 'hello world')
    s2 = SymbolicStr('s2', 'hello,world,test')
    s3 = SymbolicStr('s3', 'hello')
    
    result1 = s1.partition(' ')
    result2 = s2.partition(',')
    result3 = s3.partition(' ')
    
    print(f"  '{s1}'.partition(' ') = {result1}")
    print(f"  '{s2}'.partition(',') = {result2}")
    print(f"  '{s3}'.partition(' ') = {result3}")
    
    # 检查元组长度
    if len(result1) == 3:
        print("  ✓ partition返回三元组")
    else:
        print(f"  ✗ partition未返回三元组: 长度={len(result1)}")
    
    return True

def test_rpartition():
    """测试rpartition函数"""
    print("\n测试 rpartition 函数:")
    
    s1 = SymbolicStr('s1', 'hello world test')
    s2 = SymbolicStr('s2', 'hello,world,test')
    s3 = SymbolicStr('s3', 'hello')
    
    result1 = s1.rpartition(' ')
    result2 = s2.rpartition(',')
    result3 = s3.rpartition(' ')
    
    print(f"  '{s1}'.rpartition(' ') = {result1}")
    print(f"  '{s2}'.rpartition(',') = {result2}")
    print(f"  '{s3}'.rpartition(' ') = {result3}")
    
    return True

def test_rfind():
    """测试rfind函数"""
    print("\n测试 rfind 函数:")
    
    s1 = SymbolicStr('s1', 'hello hello world')
    s2 = SymbolicStr('s2', 'banana')
    s3 = SymbolicStr('s3', 'hello')
    
    result1 = s1.rfind('hello')
    result2 = s2.rfind('na')
    result3 = s2.rfind('na', 0, 4)
    result4 = s3.rfind('world')
    
    print(f"  '{s1}'.rfind('hello') = {result1}")
    print(f"  '{s2}'.rfind('na') = {result2}")
    print(f"  '{s2}'.rfind('na', 0, 4) = {result3}")
    print(f"  '{s3}'.rfind('world') = {result4}")
    
    return True

def test_rindex():
    """测试rindex函数"""
    print("\n测试 rindex 函数:")
    
    s1 = SymbolicStr('s1', 'hello hello world')
    s2 = SymbolicStr('s2', 'banana')
    s3 = SymbolicStr('s3', 'hello')
    
    try:
        result1 = s1.rindex('hello')
        result2 = s2.rindex('na')
        result3 = s3.rindex('world')
        print(f"  '{s1}'.rindex('hello') = {result1}")
        print(f"  '{s2}'.rindex('na') = {result2}")
        print(f"  '{s3}'.rindex('world') = {result3} (应该抛出异常)")
        # 如果没有异常，说明测试失败
        return False
    except ValueError as e:
        print(f"  正确捕获 ValueError: {e}")
        return True
    except Exception as e:
        print(f"  捕获到非预期的异常: {type(e).__name__}: {e}")
        return False

def test_existing_methods():
    """测试现有已实现的方法"""
    print("\n测试现有已实现的方法:")
    
    # 创建测试字符串
    s = SymbolicStr('test', 'Hello World')
    
    # 测试已实现的方法
    print(f"  测试字符串: '{s}'")
    
    # 大小写转换
    print(f"  .lower() = '{s.lower()}'")
    print(f"  .upper() = '{s.upper()}'")
    
    # 检查方法
    print(f"  .isalpha() = {s.isalpha()}")
    print(f"  .isdigit() = {s.isdigit()}")
    print(f"  .isalnum() = {s.isalnum()}")
    print(f"  .isnumeric() = {s.isnumeric()}")
    print(f"  .islower() = {s.islower()}")
    print(f"  .isupper() = {s.isupper()}")
    
    # 其他方法
    print(f"  .startswith('Hello') = {s.startswith('Hello')}")
    print(f"  .endswith('World') = {s.endswith('World')}")
    print(f"  .find('World') = {s.find('World')}")
    print(f"  .index('World') = {s.index('World')}")
    print(f"  .count('l') = {s.count('l')}")
    
    return True

def test_getSymbolic_str():
    """测试getSymbolic函数（字符串版）"""
    print("\n测试getSymbolic函数（字符串版）:")
    
    # 测试字符串
    result1 = getSymbolic('hello')
    result2 = getSymbolic('')
    result3 = getSymbolic('123')
    
    print(f"  getSymbolic('hello') = {result1} (类型: {type(result1)})")
    print(f"  getSymbolic('') = {result2} (类型: {type(result2)})")
    print(f"  getSymbolic('123') = {result3} (类型: {type(result3)})")
    
    # 检查是否返回SymbolicStr
    if isinstance(result1, SymbolicStr):
        print("  ✓ getSymbolic('hello') 返回 SymbolicStr")
    else:
        print("  ✗ getSymbolic('hello') 未返回 SymbolicStr")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("字符串类型扩展函数测试")
    print("=" * 60)
    
    tests = [
        test_existing_methods,
        test_getSymbolic_str,
        test_capitalize,
        test_swapcase,
        test_title,
        test_center,
        test_zfill,
        test_partition,
        test_rpartition,
        test_rfind,
        test_rindex
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                print(f"✓ {test_func.__name__} 通过")
                passed += 1
            else:
                print(f"✗ {test_func.__name__} 失败")
                failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} 出错: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试总结: 通过 {passed}, 失败 {failed}, 总计 {passed + failed}")
    
    if failed == 0:
        print("所有测试通过!")
        return 0
    else:
        print("有测试失败!")
        return 1

if __name__ == "__main__":
    sys.exit(main())