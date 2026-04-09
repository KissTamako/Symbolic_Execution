#!/usr/bin/env python
"""
调试andor.py测试失败原因
"""
import os
import sys
import subprocess
import tempfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"当前目录: {os.getcwd()}")

test_file = "test/andor.py"
print(f"测试文件: {test_file}")

# 读取andor.py内容
with open(test_file, 'r') as f:
    content = f.read()
    print(f"文件内容:\n{content}")

# 导入andor模块获取expected_result
sys.path.insert(0, '.')
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("andor", test_file)
    andor_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(andor_module)
    
    expected = andor_module.expected_result()
    print(f"expected_result(): {expected}")
    
    # 测试函数本身
    print("\n测试函数行为:")
    print(f"andor(True, True) = {andor_module.andor(True, True)}")
    print(f"andor(True, False) = {andor_module.andor(True, False)}")
    print(f"andor(False, True) = {andor_module.andor(False, True)}")
    print(f"andor(False, False) = {andor_module.andor(False, False)}")
    
except Exception as e:
    print(f"导入错误: {e}")

print("\n=== 运行pyexz3.py并捕获所有输出 ===")
# 使用-m 5减少迭代次数，方便调试
cmd = [sys.executable, 'pyexz3.py', '-m', '5', '--z3', test_file]
print(f"命令: {' '.join(cmd)}")

# 创建临时文件捕获输出
with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp:
    tmp_path = tmp.name

try:
    # 运行并捕获所有输出
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    print(f"返回码: {result.returncode}")
    
    if result.stdout:
        print("\n=== 标准输出 ===")
        print(result.stdout)
        
    if result.stderr:
        print("\n=== 错误输出 ===")
        print(result.stderr)
    
    # 分析输出
    if result.returncode == 0:
        print("\n✓ 测试通过")
        # 分析找到了哪些输入
        lines = result.stdout.split('\n')
        inputs_found = []
        for line in lines:
            if 'input' in line.lower() or 'found' in line.lower():
                print(f"相关输出: {line}")
    else:
        print("\n✗ 测试失败")
        # 尝试从输出中推断原因
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'error' in line.lower() or 'exception' in line.lower() or 'failed' in line.lower():
                    print(f"可能错误: {line}")
                    
except subprocess.TimeoutExpired:
    print("命令超时")
except Exception as e:
    print(f"执行异常: {e}")
finally:
    # 清理临时文件
    try:
        os.unlink(tmp_path)
    except:
        pass

print("\n=== 直接使用符号执行API测试 ===")
try:
    from symbolic.loader import loaderFactory
    from symbolic.explore import ExplorationEngine
    
    app = loaderFactory(test_file, 'andor', use_ast_transform=True)
    if app:
        print(f"加载成功: {app.getFile()}.{app.getEntry()}")
        inv = app.createInvocation()
        engine = ExplorationEngine(inv, solver='z3')
        
        print("开始探索...")
        generatedInputs, returnVals, path = engine.explore(5)
        
        print(f"生成的输入: {generatedInputs}")
        print(f"返回值: {returnVals}")
        
        # 与预期比较
        print(f"预期返回值: {expected}")
        
        # 检查是否找到了所有预期路径
        found_returns = list(returnVals)
        print(f"找到的返回值: {found_returns}")
        
    else:
        print("无法加载应用")
        
except Exception as e:
    print(f"符号执行API错误: {e}")
    import traceback
    traceback.print_exc()