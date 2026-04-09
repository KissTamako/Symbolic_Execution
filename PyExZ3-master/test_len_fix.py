#!/usr/bin/env python
import os
import sys

# 添加当前目录和test目录到sys.path
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('test'))

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Current dir:", os.getcwd())

try:
    # 直接使用importlib导入测试模块
    import importlib.util
    import importlib.machinery
    
    test_file = os.path.abspath('test/len_test.py')
    print(f"Testing file: {test_file}")
    
    # 方法1: 使用importlib导入
    module_name = 'test.len_test' if '.' not in test_file else test_file.replace('/', '.')[:-3]
    print(f"Module name: {module_name}")
    
    # 加载模块
    spec = importlib.util.spec_from_file_location('len_test_module', test_file)
    test_module = importlib.util.module_from_spec(spec)
    sys.modules['len_test_module'] = test_module
    spec.loader.exec_module(test_module)
    
    print("Module loaded successfully")
    print(f"Module functions: {[x for x in dir(test_module) if not x.startswith('_')]}")
    
    # 检查函数是否存在
    if hasattr(test_module, 'len_test'):
        print("Found 'len_test' function")
        func = getattr(test_module, 'len_test')
        print(f"Function: {func}")
        
        # 测试函数
        result = func(0)
        print(f"len_test(0) = {result}")
        result = func(2)
        print(f"len_test(2) = {result}")
        
    if hasattr(test_module, 'expected_result'):
        print(f"Expected result: {test_module.expected_result()}")
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()