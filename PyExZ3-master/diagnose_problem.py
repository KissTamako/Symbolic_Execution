#!/usr/bin/env python
import os
import sys
import subprocess

print("=== 诊断测试失败问题 ===")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print(f"脚本所在目录: {os.path.dirname(os.path.abspath(__file__))}")

# 检查关键文件是否存在
files_to_check = [
    'run_tests.py',
    'pyexz3.py',
    'test/simple.py',
    'symbolic/loader.py',
    'symbolic/explore.py'
]

print("\n=== 文件存在性检查 ===")
for file in files_to_check:
    exists = os.path.exists(file)
    status = '[存在]' if exists else '[缺失]'
    print(f"{status} {file}")

# 检查test目录
test_dir = 'test'
if os.path.exists(test_dir):
    print(f"\n=== test目录内容 ===")
    try:
        test_files = os.listdir(test_dir)
        py_files = [f for f in test_files if f.endswith('.py')]
        print(f"Python测试文件数量: {len(py_files)}")
        if py_files:
            print(f"前10个测试文件: {py_files[:10]}")
    except Exception as e:
        print(f"列出test目录失败: {e}")
else:
    print(f"\n[警告] test目录不存在: {test_dir}")

# 检查PYTHONPATH
print("\n=== Python路径检查 ===")
print(f"sys.path:")
for i, path in enumerate(sys.path[:10]):
    print(f"  {i}: {path}")

# 尝试导入关键模块
print("\n=== 模块导入测试 ===")
modules_to_import = [
    'symbolic.loader',
    'symbolic.explore',
    'symbolic.symbolic_types.symbolic_int',
    'symbolic.symbolic_types.symbolic_type'
]

for module_name in modules_to_import:
    try:
        __import__(module_name)
        print(f"[成功] 导入 {module_name}")
    except Exception as e:
        print(f"[失败] 导入 {module_name}: {e}")

# 尝试直接运行run_tests.py的逻辑
print("\n=== 运行run_tests.py诊断 ===")
if os.path.exists('run_tests.py'):
    try:
        # 读取run_tests.py的内容
        with open('run_tests.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查run_tests.py是否有语法错误
        try:
            compile(content, 'run_tests.py', 'exec')
            print("[成功] run_tests.py语法检查通过")
        except SyntaxError as e:
            print(f"[失败] run_tests.py语法错误: {e}")
            
        # 检查run_tests.py是否有正确的目录切换逻辑
        if 'ensure_in_correct_directory' in content or 'os.chdir' in content:
            print("[成功] run_tests.py包含目录切换逻辑")
        else:
            print("[警告] run_tests.py可能不包含目录切换逻辑")
            
    except Exception as e:
        print(f"[错误] 读取run_tests.py失败: {e}")
else:
    print("[错误] run_tests.py文件不存在")

# 尝试最简单的符号执行测试
print("\n=== 简单符号执行测试 ===")
if os.path.exists('test/simple.py'):
    try:
        # 直接使用loaderFactory
        import symbolic.loader
        from symbolic.explore import ExplorationEngine
        
        print("[成功] 导入符号执行核心模块")
        
        # 尝试创建loader
        app = symbolic.loader.loaderFactory('test/simple.py', 'simple', use_ast_transform=False)
        if app:
            print("[成功] 创建Loader对象")
            # 创建执行引擎但不运行
            engine = ExplorationEngine(app.createInvocation(), solver='z3')
            print("[成功] 创建ExplorationEngine对象")
            print("[信息] 基础符号执行框架看起来正常")
        else:
            print("[失败] loaderFactory返回None")
            
    except Exception as e:
        print(f"[失败] 符号执行测试出错: {e}")
        import traceback
        traceback.print_exc()
else:
    print("[跳过] test/simple.py不存在")

print("\n=== 总结 ===")
print("1. 确保在PyExZ3-master目录下运行命令")
print("2. 检查run_tests.py是否有语法错误")
print("3. 验证test目录存在且包含测试文件")
print("4. 检查符号执行核心模块是否能正常导入")