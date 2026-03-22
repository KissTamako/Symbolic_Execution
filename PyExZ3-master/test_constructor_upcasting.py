#!/usr/bin/env python3
"""测试内置构造函数符号化功能"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_ast_transformation():
    """测试AST转换功能"""
    print("测试AST转换:")
    
    test_cases = [
        # (原始代码, 期望转换片段)
        ('int(x)', 'SymbolicInteger.from_symbolic'),
        ('str(x)', 'SymbolicStr.from_symbolic'),
        ('range(1, 10)', 'SymbolicRange.from_symbolic'),
        ('float(x)', 'SymbolicFloat.from_symbolic'),
        ('bool(x)', 'SymbolicInteger.from_symbolic'),  # bool使用SymbolicInteger
    ]
    
    from symbolic.ast_upcaster import transform_source_code
    
    for i, (original, expected_snippet) in enumerate(test_cases):
        transformed_source, _ = transform_source_code(original)
        print(f"测试 {i+1}:")
        print(f"  原始: {original}")
        print(f"  转换: {transformed_source[:100] if transformed_source else '<无输出>'}") 
        print(f"  期望包含: {expected_snippet}")
        
        if transformed_source and expected_snippet in transformed_source:
            print(f"  ✓ 包含 {expected_snippet}")
        else:
            print(f"  ✗ 不包含 {expected_snippet}")
        print()

def test_direct_constructor():
    """直接测试构造函数符号化"""
    print("\n直接测试构造函数符号化:")
    
    try:
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        from symbolic.symbolic_types.symbolic_str import SymbolicStr
        from symbolic.symbolic_types.symbolic_range import SymbolicRange
        
        # 创建符号整数
        x = SymbolicInteger("x", 5)
        
        # 测试int()构造函数
        print(f"1. 测试int()构造函数:")
        print(f"  原始x: {x}, 类型: {type(x)}")
        
        # 如果from_symbolic方法存在，测试它
        if hasattr(SymbolicInteger, 'from_symbolic'):
            result = SymbolicInteger.from_symbolic(x)
            print(f"  SymbolicInteger.from_symbolic(x): {result}, 类型: {type(result)}")
        else:
            print(f"  ✗ SymbolicInteger.from_symbolic() 方法不存在")
        
        # 测试str()构造函数
        print(f"\n2. 测试str()构造函数:")
        if hasattr(SymbolicStr, 'from_symbolic'):
            result = SymbolicStr.from_symbolic(x)
            print(f"  SymbolicStr.from_symbolic(x): {result}, 类型: {type(result)}")
        else:
            print(f"  ✗ SymbolicStr.from_symbolic() 方法不存在")
        
        # 测试range()构造函数
        print(f"\n3. 测试range()构造函数:")
        if hasattr(SymbolicRange, 'from_symbolic'):
            # 测试两个参数版本
            start = SymbolicInteger("start", 1)
            stop = SymbolicInteger("stop", 10)
            result = SymbolicRange.from_symbolic(start, stop)
            print(f"  SymbolicRange.from_symbolic({start}, {stop}): {result}, 类型: {type(result)}")
        else:
            print(f"  ✗ SymbolicRange.from_symbolic() 方法不存在")
            
    except Exception as e:
        print(f"  ✗ 测试出错: {e}")
        import traceback
        traceback.print_exc()

def test_with_loader():
    """通过loader测试构造函数符号化"""
    print("\n通过loader测试构造函数符号化:")
    
    # 创建测试文件
    test_code = '''from symbolic.symbolic_types.symbolic_int import SymbolicInteger

def test_func():
    x = SymbolicInteger("x", 5)
    # 测试int()构造函数，应被转换为SymbolicInteger.from_symbolic(x)
    result = int(x)
    return result
'''
    
    # 写入临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # 通过loader加载和执行
        from symbolic.loader import loaderFactory
        loader = loaderFactory(temp_file, "test_func")
        if not loader:
            print("  ✗ loader创建失败")
            return
        
        inv = loader.createInvocation()
        result = inv.callFunction({})
        
        print(f"  int(SymbolicInteger('x', 5)) = {result}")
        print(f"  结果类型: {type(result).__name__}")
        
        # 检查是否是符号类型
        if hasattr(result, 'getConcrValue'):
            print(f"  ✓ 构造函数符号化生效！结果是符号类型")
            print(f"  具体值: {result.getConcrValue()}")
        else:
            print(f"  ✗ 构造函数符号化未生效！结果是普通{type(result).__name__}")
            
    except Exception as e:
        print(f"  ✗ loader测试出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        import os
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def main():
    """主函数"""
    print("=" * 60)
    print("内置构造函数符号化测试")
    print("=" * 60)
    
    test_ast_transformation()
    test_direct_constructor()
    test_with_loader()
    
    print("\n" + "=" * 60)
    print("测试完成")

if __name__ == "__main__":
    main()