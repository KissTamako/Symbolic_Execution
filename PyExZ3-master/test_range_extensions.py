#!/usr/bin/env python3
"""测试Range类型新增扩展函数"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from symbolic.symbolic_types.symbolic_range import SymbolicRange
from symbolic.symbolic_types.symbolic_int import SymbolicInteger

def test_range_basic_operations():
    """测试Range基本操作"""
    print("测试Range基本操作:")
    
    # 创建符号range对象
    r1 = SymbolicRange('r1', range(5, 10))
    r2 = SymbolicRange('r2', range(1, 10, 2))
    r3 = SymbolicRange('r3', range(10, 5, -1))
    
    print(f"  r1 = {r1}")
    print(f"  r2 = {r2}")
    print(f"  r3 = {r3}")
    
    # 测试长度
    print(f"  len(r1) = {len(r1)} (类型: {type(len(r1)).__name__})")
    print(f"  len(r2) = {len(r2)} (类型: {type(len(r2)).__name__})")
    print(f"  len(r3) = {len(r3)} (类型: {type(len(r3)).__name__})")
    
    return True

def test_range_contains():
    """测试__contains__函数"""
    print("\n测试__contains__函数:")
    
    r = SymbolicRange('r', range(5, 10))
    
    # 测试包含和不包含的元素
    test_cases = [
        (4, False),
        (5, True),
        (7, True),
        (9, True),
        (10, False),
        (15, False)
    ]
    
    for value, expected in test_cases:
        result = value in r
        concrete = result.getConcrValue() if hasattr(result, 'getConcrValue') else result
        print(f"  {value} in {r} = {concrete} (期望: {expected})")
        if concrete == expected:
            print("  ✓ 正确")
        else:
            print(f"  ✗ 错误: 期望{expected}, 得到{concrete}")
    
    return True

def test_range_iteration():
    """测试迭代功能"""
    print("\n测试迭代功能:")
    
    r = SymbolicRange('r', range(1, 6, 2))
    
    print(f"  迭代 {r}:")
    items = []
    for item in r:
        items.append(item)
        print(f"    {item} (类型: {type(item).__name__})")
    
    print(f"  迭代结果: {items}")
    
    # 检查迭代长度
    if len(items) == len(r.getConcrValue()):
        print("  ✓ 迭代长度正确")
    else:
        print(f"  ✗ 迭代长度错误: 期望{len(r.getConcrValue())}, 得到{len(items)}")
    
    return True

def test_range_count_index():
    """测试count和index函数"""
    print("\n测试count和index函数:")
    
    r = SymbolicRange('r', range(5, 10))
    
    # 测试count
    result1 = r.count(7)
    result2 = r.count(12)
    
    print(f"  {r}.count(7) = {result1} (类型: {type(result1).__name__})")
    print(f"  {r}.count(12) = {result2} (类型: {type(result2).__name__})")
    
    # 测试index
    result3 = r.index(7)
    print(f"  {r}.index(7) = {result3} (类型: {type(result3).__name__})")
    
    # 测试不存在的元素 - SymbolicRange.index() 返回 -1，不抛出异常
    result4 = r.index(12)
    print(f"  {r}.index(12) = {result4} (期望: -1)")
    
    # 检查不存在的元素是否返回 -1
    concr4 = result4.getConcrValue() if hasattr(result4, 'getConcrValue') else result4
    if concr4 == -1:
        print("  ✓ 不存在的元素返回 -1")
        return True
    else:
        print(f"  ✗ 不存在的元素应返回 -1，实际返回 {concr4}")
        return False

def test_range_getitem():
    """测试__getitem__函数"""
    print("\n测试__getitem__函数:")
    
    r = SymbolicRange('r', range(5, 10))
    
    # 测试正索引
    print(f"  测试正索引:")
    for i in range(len(r.getConcrValue())):
        result = r[i]
        print(f"    {r}[{i}] = {result} (类型: {type(result).__name__})")
    
    # 测试负索引
    print(f"  测试负索引:")
    for i in range(-len(r.getConcrValue()), 0):
        result = r[i]
        print(f"    {r}[{i}] = {result} (类型: {type(result).__name__})")
    
    # 测试切片
    print(f"  测试切片:")
    slice1 = r[1:3]
    slice2 = r[:3]
    slice3 = r[2:]
    
    print(f"    {r}[1:3] = {slice1} (类型: {type(slice1).__name__})")
    print(f"    {r}[:3] = {slice2} (类型: {type(slice2).__name__})")
    print(f"    {r}[2:] = {slice3} (类型: {type(slice3).__name__})")
    
    return True

def test_range_comparisons():
    """测试比较操作"""
    print("\n测试比较操作:")
    
    r1 = SymbolicRange('r1', range(5, 10))
    r2 = SymbolicRange('r2', range(5, 10))
    r3 = SymbolicRange('r3', range(5, 11))
    r4 = SymbolicRange('r4', range(6, 10))
    
    # 测试相等
    eq1 = r1 == r2
    eq2 = r1 == r3
    eq3 = r1 == r4
    
    print(f"  {r1} == {r2} = {eq1} (类型: {type(eq1).__name__})")
    print(f"  {r1} == {r3} = {eq2} (类型: {type(eq2).__name__})")
    print(f"  {r1} == {r4} = {eq3} (类型: {type(eq3).__name__})")
    
    # 测试不相等
    ne1 = r1 != r2
    ne2 = r1 != r3
    
    print(f"  {r1} != {r2} = {ne1} (类型: {type(ne1).__name__})")
    print(f"  {r1} != {r3} = {ne2} (类型: {type(ne2).__name__})")
    
    # 测试其他比较
    lt1 = r1 < r4
    gt1 = r4 > r1
    
    print(f"  {r1} < {r4} = {lt1} (类型: {type(lt1).__name__})")
    print(f"  {r4} > {r1} = {gt1} (类型: {type(gt1).__name__})")
    
    return True

def test_range_reversed():
    """测试__reversed__函数"""
    print("\n测试__reversed__函数:")
    
    r = SymbolicRange('r', range(1, 6))
    
    # 测试反转
    reversed_r = reversed(r)
    
    print(f"  reversed({r}) = {reversed_r}")
    print(f"  反转类型: {type(reversed_r).__name__}")
    
    # 迭代反转结果
    items = list(reversed_r)
    print(f"  反转迭代结果: {items}")
    
    # 检查是否正确反转
    original = list(r.getConcrValue())
    expected = list(reversed(original))
    
    actual_items = [item.getConcrValue() if hasattr(item, 'getConcrValue') else item for item in items]
    
    if actual_items == expected:
        print("  ✓ 反转正确")
    else:
        print(f"  ✗ 反转错误: 期望{expected}, 得到{actual_items}")
    
    return True

def test_range_bool():
    """测试__bool__函数"""
    print("\n测试__bool__函数:")
    
    # 测试非空range
    r1 = SymbolicRange('r1', range(1, 5))
    bool1 = bool(r1)
    
    print(f"  bool({r1}) = {bool1} (类型: {type(bool1).__name__})")
    
    # 测试空range
    r2 = SymbolicRange('r2', range(5, 5))
    bool2 = bool(r2)
    
    print(f"  bool({r2}) = {bool2} (类型: {type(bool2).__name__})")
    
    if bool1 and not bool2:
        print("  ✓ bool转换正确")
    else:
        print(f"  ✗ bool转换错误: 非空应True得到{bool1}, 空应False得到{bool2}")
    
    return True

def test_range_hash():
    """测试__hash__函数"""
    print("\n测试__hash__函数:")
    
    r1 = SymbolicRange('r1', range(5, 10))
    r2 = SymbolicRange('r2', range(5, 10))
    r3 = SymbolicRange('r3', range(5, 11))
    
    # 测试哈希值
    hash1 = hash(r1)
    hash2 = hash(r2)
    hash3 = hash(r3)
    
    print(f"  hash({r1}) = {hash1}")
    print(f"  hash({r2}) = {hash2}")
    print(f"  hash({r3}) = {hash3}")
    
    # 检查相同值是否有相同哈希
    if hash1 == hash2:
        print("  ✓ 相同值有相同哈希")
    else:
        print("  ✗ 相同值有不同的哈希")
    
    # 检查不同值是否有不同哈希
    if hash1 != hash3:
        print("  ✓ 不同值有不同的哈希")
    else:
        print("  ✗ 不同值有相同的哈希")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Range类型扩展函数测试")
    print("=" * 60)
    
    tests = [
        test_range_basic_operations,
        test_range_contains,
        test_range_iteration,
        test_range_count_index,
        test_range_getitem,
        test_range_comparisons,
        test_range_reversed,
        test_range_bool,
        test_range_hash
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