#!/usr/bin/env python3
"""测试常量提升的演示程序"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_with_loader():
    """通过loader测试常量提升"""
    # 创建测试文件
    test_code = '''from symbolic.symbolic_types.symbolic_int import SymbolicInteger

def test_func():
    x = SymbolicInteger("x", 3)
    # 测试常量方法调用
    # 如果常量提升生效，这应该返回SymbolicInteger而不是int
    result = (5).__add__(x)
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
            print("✗ loader创建失败")
            return None
        
        inv = loader.createInvocation()
        result = inv.callFunction({})
        
        print(f"(5).__add__(x) = {result}, type: {type(result)}")
        
        # 检查是否是符号类型
        if hasattr(result, 'getConcrValue'):
            print(f"✓ 常量提升生效！结果是SymbolicInteger，具体值: {result.getConcrValue()}")
        else:
            print(f"✗ 常量提升未生效！结果是普通{type(result).__name__}: {result}")
        
        return result
    finally:
        import os
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_direct():
    """直接测试（用于对比）"""
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    
    x = SymbolicInteger("x", 3)
    
    # 直接调用（不会触发常量提升，因为不是通过loader加载的）
    result = (5).__add__(x)
    print(f"直接调用: (5).__add__(x) = {result}, type: {type(result)}")
    
    if hasattr(result, 'getConcrValue'):
        print(f"  直接调用结果类型: SymbolicInteger")
    else:
        print(f"  直接调用结果类型: {type(result).__name__}")
    
    return result

if __name__ == "__main__":
    print("="*60)
    print("常量提升技术演示")
    print("="*60)
    
    print("\n1. 直接调用（不通过loader，常量提升不生效）:")
    test_direct()
    
    print("\n2. 通过loader调用（常量提升生效）:")
    test_with_loader()
    
    print("\n" + "="*60)
    print("总结：常量提升技术仅在通过loader加载代码时生效")
    print("="*60)
