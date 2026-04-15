import sys
import traceback

# 确保能导入symbolic模块
sys.path.insert(0, '.')

try:
    print("Testing symbolic types...")
    
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
    
    # 测试__index__方法
    print(f"__index__: {x.__index__()}")
    
    # 测试__sizeof__方法
    print(f"__sizeof__: {x.__sizeof__()}")
    
    # 测试__complex__方法
    print(f"__complex__: {x.__complex__()}")
    
    # 测试__float__方法
    print(f"__float__: {x.__float__()}")
    
    # 测试__str__方法
    print(f"__str__: {x.__str__()}")
    
    # 测试__repr__方法
    print(f"__repr__: {x.__repr__()}")
    
    # 测试__pow__方法（带错误处理）
    print("Testing __pow__ method...")
    try:
        result = x.__pow__(2)
        print(f"x ** 2: {result}")
    except Exception as e:
        print(f"Error in __pow__: {e}")
    
    # 测试SymbolicFloat类的新方法
    print("\n3. Testing SymbolicFloat methods...")
    
    # 创建一个SymbolicFloat对象
    y = SymbolicFloat("y", 3.14)
    print(f"Created SymbolicFloat: {y}")
    
    # 测试__index__方法
    print(f"__index__: {y.__index__()}")
    
    # 测试__sizeof__方法
    print(f"__sizeof__: {y.__sizeof__()}")
    
    # 测试__complex__方法
    print(f"__complex__: {y.__complex__()}")
    
    # 测试__str__方法
    print(f"__str__: {y.__str__()}")
    
    # 测试__repr__方法
    print(f"__repr__: {y.__repr__()}")
    
    # 测试__rlt__方法
    print(f"__rlt__ (5 < y): {y.__rlt__(5)}")
    
    # 测试__rle__方法
    print(f"__rle__ (5 <= y): {y.__rle__(5)}")
    
    # 测试__rgt__方法
    print(f"__rgt__ (5 > y): {y.__rgt__(5)}")
    
    # 测试__rge__方法
    print(f"__rge__ (5 >= y): {y.__rge__(5)}")
    
    # 测试SymbolicStr类的新方法
    print("\n4. Testing SymbolicStr methods...")
    
    # 创建一个SymbolicStr对象
    s = SymbolicStr("s", "Hello, World!")
    print(f"Created SymbolicStr: {s}")
    
    # 测试casefold方法
    print(f"casefold: {s.casefold()}")
    
    # 测试format方法
    print(f"format: {s.format()}")
    
    # 测试join方法
    print(f"join: {s.join(['a', 'b', 'c'])}")
    
    # 测试partition方法
    print(f"partition: {s.partition(',')}")
    
    # 测试rfind方法
    print(f"rfind: {s.rfind('o')}")
    
    # 测试rpartition方法
    print(f"rpartition: {s.rpartition('o')}")
    
    # 测试rsplit方法
    print(f"rsplit: {s.rsplit(' ')}")
    
    # 测试rstrip方法
    print(f"rstrip: {s.rstrip('!')}")
    
    # 测试splitlines方法
    print(f"splitlines: {s.splitlines()}")
    
    # 测试swapcase方法
    print(f"swapcase: {s.swapcase()}")
    
    # 测试title方法
    print(f"title: {s.title()}")
    
    # 测试__complex__方法（带错误处理）
    print("Testing __complex__ method...")
    try:
        result = s.__complex__()
        print(f"__complex__: {result}")
    except Exception as e:
        print(f"Error in __complex__: {e}")
    
    # 测试__float__方法（带错误处理）
    print("Testing __float__ method...")
    try:
        result = s.__float__()
        print(f"__float__: {result}")
    except Exception as e:
        print(f"Error in __float__: {e}")
    
    # 测试__int__方法（带错误处理）
    print("Testing __int__ method...")
    try:
        result = s.__int__()
        print(f"__int__: {result}")
    except Exception as e:
        print(f"Error in __int__: {e}")
    
    # 测试__repr__方法
    print(f"__repr__: {s.__repr__()}")
    
    print("\nAll tests completed!")
    
except Exception as e:
    print(f"\nError: {e}")
    traceback.print_exc()