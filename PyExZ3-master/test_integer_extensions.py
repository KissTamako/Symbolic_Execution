#!/usr/bin/env python3
"""测试整数类型新增扩展函数"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types import getSymbolic

def test_divmod():
    """测试divmod函数"""
    print("测试 divmod 函数:")
    
    # 创建符号整数
    a = SymbolicInteger('a', 10)
    b = SymbolicInteger('b', 3)
    
    # 测试divmod
    result = divmod(a, b)
    print(f"  divmod({a}, {b}) = {result}")
    
    # 测试反向divmod
    result2 = divmod(10, b)
    print(f"  divmod(10, {b}) = {result2}")
    
    # 检查结果类型
    print(f"  结果类型: {type(result)}")
    print(f"  元组内容: {result[0]}, {result[1]}")
    
    return True

def test_invert():
    """测试位取反操作符"""
    print("\n测试位取反操作符 (~):")
    
    a = SymbolicInteger('a', 42)
    result = ~a
    
    print(f"  ~{a} = {result}")
    print(f"  位取反具体值: ~42 = {~42}")
    print(f"  结果类型: {type(result)}")
    
    # 检查是否创建了正确的表达式
    if not result.isVariable():
        print(f"  表达式树: {result.expr}")
    
    return True

def test_format():
    """测试format函数"""
    print("\n测试format函数:")
    
    a = SymbolicInteger('a', 42)
    
    # 测试不同格式化方式
    result1 = format(a, "d")
    result2 = format(a, "x")
    result3 = format(a, "b")
    result4 = format(a, "o")
    
    print(f"  format({a}, 'd') = {result1}")
    print(f"  format({a}, 'x') = {result2}")
    print(f"  format({a}, 'b') = {result3}")
    print(f"  format({a}, 'o') = {result4}")
    
    # 检查结果类型
    print(f"  结果类型: {type(result1)}")
    
    return True

def test_index():
    """测试__index__函数"""
    print("\n测试__index__函数:")
    
    a = SymbolicInteger('a', 42)
    
    # 测试__index__
    result = a.__index__()
    
    print(f"  {a}.__index__() = {result}")
    print(f"  结果类型: {type(result)}")
    print(f"  具体值: {result}")
    
    # 测试在切片中使用
    lst = [0, 1, 2, 3, 4, 5]
    try:
        slice_result = lst[a.__index__()]
        print(f"  在切片中使用: lst[{a.__index__()}] = {slice_result}")
    except IndexError:
        print(f"  在切片中使用: 索引超出范围")
    
    return True

def test_as_integer_ratio():
    """测试as_integer_ratio函数"""
    print("\n测试as_integer_ratio函数:")
    
    a = SymbolicInteger('a', 42)
    
    # 测试as_integer_ratio
    result = a.as_integer_ratio()
    
    print(f"  {a}.as_integer_ratio() = {result}")
    print(f"  结果类型: {type(result)}")
    print(f"  元组内容: {result[0]}, {result[1]}")
    
    # 检查比例是否正确
    if result[1].getConcrValue() == 1:
        print("  ✓ 分母为1，正确")
    else:
        print("  ✗ 分母不为1，错误")
    
    return True

def test_bit_length():
    """测试bit_length函数"""
    print("\n测试bit_length函数:")
    
    # 测试不同数字的位长度
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 2),
        (42, 6),
        (255, 8),
        (256, 9),
        (-1, 1),  # 负数在二进制补码中的表示
        (-42, 6)
    ]
    
    for value, expected in test_cases:
        a = SymbolicInteger(f'num{value}', value)
        result = a.bit_length()
        concrete = result.getConcrValue() if hasattr(result, 'getConcrValue') else result
        
        print(f"  {value}.bit_length() = {concrete} (期望: {expected})")
        if concrete == expected:
            print("  ✓ 正确")
        else:
            print(f"  ✗ 错误: 期望{expected}, 得到{concrete}")
    
    return True

def test_to_bytes():
    """测试to_bytes函数"""
    print("\n测试to_bytes函数:")
    
    a = SymbolicInteger('a', 42)
    
    # 测试to_bytes
    result1 = a.to_bytes(1, 'big')
    result2 = a.to_bytes(2, 'big')
    result3 = a.to_bytes(1, 'little')
    
    print(f"  {a}.to_bytes(1, 'big') = {result1}")
    print(f"  {a}.to_bytes(2, 'big') = {result2}")
    print(f"  {a}.to_bytes(1, 'little') = {result3}")
    
    # 检查结果类型
    print(f"  结果类型: {type(result1)}")
    
    # 测试大数
    b = SymbolicInteger('b', 65535)
    result4 = b.to_bytes(2, 'big')
    print(f"  65535.to_bytes(2, 'big') = {result4}")
    
    return True

def test_hash():
    """测试__hash__函数"""
    print("\n测试__hash__函数:")
    
    a = SymbolicInteger('a', 42)
    b = SymbolicInteger('b', 42)
    c = SymbolicInteger('c', 43)
    
    # 测试哈希值
    hash_a = hash(a)
    hash_b = hash(b)
    hash_c = hash(c)
    
    print(f"  hash({a}) = {hash_a}")
    print(f"  hash({b}) = {hash_b}")
    print(f"  hash({c}) = {hash_c}")
    
    # 检查相同值是否有相同哈希
    if hash_a == hash_b:
        print("  ✓ 相同值有相同哈希")
    else:
        print("  ✗ 相同值有不同的哈希")
    
    # 检查不同值是否有不同哈希
    if hash_a != hash_c:
        print("  ✓ 不同值有不同的哈希")
    else:
        print("  ✗ 不同值有相同的哈希")
    
    return True

def test_getSymbolic():
    """测试getSymbolic函数"""
    print("\n测试getSymbolic函数:")
    
    # 测试整数
    result1 = getSymbolic(42)
    result2 = getSymbolic(-10)
    result3 = getSymbolic(0)
    
    print(f"  getSymbolic(42) = {result1} (类型: {type(result1)})")
    print(f"  getSymbolic(-10) = {result2} (类型: {type(result2)})")
    print(f"  getSymbolic(0) = {result3} (类型: {type(result3)})")
    
    # 检查是否返回SymbolicInteger
    if isinstance(result1, SymbolicInteger):
        print("  ✓ getSymbolic(42) 返回 SymbolicInteger")
    else:
        print("  ✗ getSymbolic(42) 未返回 SymbolicInteger")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("整数类型扩展函数测试")
    print("=" * 60)
    
    tests = [
        test_divmod,
        test_invert,
        test_format,
        test_index,
        test_as_integer_ratio,
        test_bit_length,
        test_to_bytes,
        test_hash,
        test_getSymbolic
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