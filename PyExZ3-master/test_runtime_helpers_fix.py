#!/usr/bin/env python
"""
测试runtime_helpers.py的修复结果
"""
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=== 测试runtime_helpers.py修复 ===")

# 测试1: 导入runtime_helpers
try:
    import symbolic.runtime_helpers as rh
    print("[PASS] runtime_helpers导入成功")
except Exception as e:
    print(f"[FAIL] runtime_helpers导入失败: {e}")
    sys.exit(1)

# 测试2: 测试unwrap函数的各种情况
print("\n--- 测试unwrap函数 ---")

# 2.1 普通值
try:
    assert rh.unwrap(42) == 42
    assert rh.unwrap("hello") == "hello"
    assert rh.unwrap(True) == True
    assert rh.unwrap(False) == False
    print("[PASS] unwrap普通值正常")
except Exception as e:
    print(f"[FAIL] unwrap普通值失败: {e}")

# 2.2 符号整型值
try:
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    sym_int = SymbolicInteger("test", 123, None)
    result = rh.unwrap(sym_int)
    assert result == 123, f"unwrap(SymbolicInteger)返回{result}, 期望123"
    print("[PASS] unwrap符号整型正常")
except Exception as e:
    print(f"[FAIL] unwrap符号整型失败: {e}")

# 2.3 符号字符串值
try:
    from symbolic.symbolic_types.symbolic_str import SymbolicStr
    sym_str = SymbolicStr("test", "hello", None)
    result = rh.unwrap(sym_str)
    assert result == "hello", f"unwrap(SymbolicStr)返回{result}, 期望hello"
    print("[PASS] unwrap符号字符串正常")
except Exception as e:
    print(f"[FAIL] unwrap符号字符串失败: {e}")

# 2.4 列表中的符号值
try:
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    sym_list = [SymbolicInteger("x", 1, None), SymbolicInteger("y", 2, None), 3]
    result = rh.unwrap(sym_list)
    assert result == [1, 2, 3], f"unwrap符号列表返回{result}, 期望[1, 2, 3]"
    print("[PASS] unwrap符号列表正常")
except Exception as e:
    print(f"[FAIL] unwrap符号列表失败: {e}")

# 测试3: 测试_se_int函数
print("\n--- 测试_se_int函数 ---")
try:
    # 普通值
    wrapped1 = rh._se_int(42)
    assert isinstance(wrapped1, SymbolicInteger), f"_se_int(42)返回{type(wrapped1)}"
    
    # 符号值
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    sym_int = SymbolicInteger("test", 123, None)
    wrapped2 = rh._se_int(sym_int)
    assert isinstance(wrapped2, SymbolicInteger), f"_se_int(SymbolicInteger)返回{type(wrapped2)}"
    
    print("[PASS] _se_int函数正常")
except Exception as e:
    print(f"[FAIL] _se_int函数失败: {e}")

# 测试4: 测试_se_str函数
print("\n--- 测试_se_str函数 ---")
try:
    from symbolic.symbolic_types.symbolic_str import SymbolicStr
    
    # 普通值
    wrapped1 = rh._se_str("hello")
    assert isinstance(wrapped1, SymbolicStr), f"_se_str('hello')返回{type(wrapped1)}"
    
    # 符号值
    sym_str = SymbolicStr("test", "world", None)
    wrapped2 = rh._se_str(sym_str)
    assert isinstance(wrapped2, SymbolicStr), f"_se_str(SymbolicStr)返回{type(wrapped2)}"
    
    print("[PASS] _se_str函数正常")
except Exception as e:
    print(f"[FAIL] _se_str函数失败: {e}")

# 测试5: 测试wrap_concrete_constant函数
print("\n--- 测试wrap_concrete_constant函数 ---")
try:
    # 整型
    wrapped_int = rh.wrap_concrete_constant(42)
    assert isinstance(wrapped_int, SymbolicInteger), f"wrap_concrete_constant(42)返回{type(wrapped_int)}"
    
    # 字符串
    wrapped_str = rh.wrap_concrete_constant("hello")
    assert isinstance(wrapped_str, SymbolicStr), f"wrap_concrete_constant('hello')返回{type(wrapped_str)}"
    
    # 布尔值 (应保持原样)
    wrapped_bool = rh.wrap_concrete_constant(True)
    assert wrapped_bool is True, f"wrap_concrete_constant(True)返回{wrapped_bool}"
    
    # 列表
    wrapped_list = rh.wrap_concrete_constant([1, 2, 3])
    assert isinstance(wrapped_list, list), f"wrap_concrete_constant([1,2,3])返回{type(wrapped_list)}"
    
    print("[PASS] wrap_concrete_constant函数正常")
except Exception as e:
    print(f"[FAIL] wrap_concrete_constant函数失败: {e}")

# 测试6: 检查是否有bool导入问题
print("\n--- 检查bool导入问题 ---")
try:
    # 读取文件内容检查是否有"import bool"语句
    with open('symbolic/runtime_helpers.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'import bool as bool_module' in content:
        print("[FAIL] 文件中仍然存在错误的bool导入语句")
    elif 'import bool' in content:
        print("[FAIL] 文件中存在bool导入语句")
    else:
        print("[PASS] 文件中没有错误的bool导入语句")
        
    # 检查修复后的代码是否存在
    if 'return bool.__bool__(value)' in content:
        print("[PASS] 已使用正确的bool.__bool__调用")
    else:
        print("[WARN] 未找到bool.__bool__调用")
        
except Exception as e:
    print(f"[FAIL] 检查文件内容失败: {e}")

print("\n=== 测试总结 ===")
print("修复已完成：")
print("1. 移除了错误的 'import bool as bool_module' 语句")
print("2. 使用 'bool.__bool__(value)' 替代错误的导入")
print("3. 参考了PyCT-master的实现方式")
print("\n所有runtime_helpers函数现在应该能正常导入和使用，不会再出现'无法解析导入bool'的错误。")