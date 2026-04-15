import sys
import traceback

# 确保能导入symbolic模块
sys.path.insert(0, '.')

try:
    print("Testing enhanced symbolic types...")
    
    # 测试导入核心模块
    print("1. Importing symbolic types...")
    from symbolic.symbolic_types.symbolic_int import SymbolicInteger
    from symbolic.symbolic_types.symbolic_float import SymbolicFloat
    from symbolic.symbolic_types.symbolic_str import SymbolicStr
    print("Symbolic types imported successfully")
    
    # 测试SymbolicInteger类的新方法
    print("\n2. Testing SymbolicInteger methods...")
    
    # 创建一个SymbolicInteger对象
    x = SymbolicInteger("x", 42)
    print(f"Created SymbolicInteger: {x}")
    
    # 测试__floor__方法
    print(f"__floor__: {x.__floor__()}")
    
    # 测试__ceil__方法
    print(f"__ceil__: {x.__ceil__()}")
    
    # 测试from_bytes方法（正常情况）
    print("Testing from_bytes method...")
    try:
        bytes_data = b'\x2a'
        result = SymbolicInteger.from_bytes(bytes_data, 'big')
        print(f"from_bytes: {result}")
    except Exception as e:
        print(f"Error in from_bytes: {e}")
    
    # 测试from_bytes方法（错误情况）
    print("Testing from_bytes method with error...")
    try:
        result = SymbolicInteger.from_bytes("not bytes", 'big')
        print(f"from_bytes: {result}")
    except Exception as e:
        print(f"Expected error in from_bytes: {e}")
    
    # 测试SymbolicFloat类的新方法
    print("\n3. Testing SymbolicFloat methods...")
    
    # 创建一个SymbolicFloat对象
    y = SymbolicFloat("y", 3.14)
    print(f"Created SymbolicFloat: {y}")
    
    # 测试__str2__方法
    print(f"__str2__: {y.__str2__()}")
    
    # 测试__truediv__方法（正常情况）
    print("Testing __truediv__ method...")
    try:
        z = SymbolicFloat("z", 2.0)
        result = y.__truediv__(z)
        print(f"y / z: {result}")
    except Exception as e:
        print(f"Error in __truediv__: {e}")
    
    # 测试__truediv__方法（除零错误）
    print("Testing __truediv__ method with division by zero...")
    try:
        z = SymbolicFloat("z", 0.0)
        result = y.__truediv__(z)
        print(f"y / z: {result}")
    except Exception as e:
        print(f"Expected error in __truediv__: {e}")
    
    # 测试__pow__方法（正常情况）
    print("Testing __pow__ method...")
    try:
        z = SymbolicFloat("z", 2.0)
        result = y.__pow__(z)
        print(f"y ** z: {result}")
    except Exception as e:
        print(f"Error in __pow__: {e}")
    
    # 测试SymbolicStr类的新方法
    print("\n4. Testing SymbolicStr methods...")
    
    # 创建一个SymbolicStr对象
    s = SymbolicStr("s", "123")
    print(f"Created SymbolicStr: {s}")
    
    # 测试__float2__方法（正常情况）
    print("Testing __float2__ method...")
    try:
        result = s.__float2__()
        print(f"__float2__: {result}")
    except Exception as e:
        print(f"Error in __float2__: {e}")
    
    # 测试__float2__方法（错误情况）
    print("Testing __float2__ method with error...")
    try:
        s_error = SymbolicStr("s_error", "not a float")
        result = s_error.__float2__()
        print(f"__float2__: {result}")
    except Exception as e:
        print(f"Expected error in __float2__: {e}")
    
    # 测试__int2__方法（正常情况）
    print("Testing __int2__ method...")
    try:
        result = s.__int2__()
        print(f"__int2__: {result}")
    except Exception as e:
        print(f"Error in __int2__: {e}")
    
    # 测试__int2__方法（错误情况）
    print("Testing __int2__ method with error...")
    try:
        s_error = SymbolicStr("s_error", "not an int")
        result = s_error.__int2__()
        print(f"__int2__: {result}")
    except Exception as e:
        print(f"Expected error in __int2__: {e}")
    
    print("\nAll tests completed!")
    
except Exception as e:
    print(f"\nError: {e}")
    traceback.print_exc()