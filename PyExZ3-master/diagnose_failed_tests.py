#!/usr/bin/env python
"""
诊断9个失败测试的具体错误
"""
import os
import sys
import subprocess
import traceback

# 确保在PyExZ3-master目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print(f"当前目录: {os.getcwd()}")
print(f"脚本目录: {script_dir}")

# 9个失败的测试文件
failed_tests = [
    'andor.py',
    'bignum.py',
    'decorator.py',
    'decorator_dict.py',
    'diamond.py',
    'filesys.py',
    'fp.py',
    'gcd.py',
    'len_test.py'
]

# 检查测试文件是否存在
print("\n=== 检查测试文件是否存在 ===")
for test in failed_tests:
    test_path = os.path.join('test', test)
    exists = os.path.exists(test_path)
    status = '✓' if exists else '✗'
    print(f"  {status} {test_path}: {'存在' if exists else '不存在'}")

print("\n" + "="*60 + "\n")

# 逐个运行测试，捕获详细错误
for test in failed_tests:
    test_path = os.path.join('test', test)
    if not os.path.exists(test_path):
        print(f"✗ {test}: 测试文件不存在")
        continue
    
    print(f"=== 测试: {test} ===")
    
    # 方法1: 使用run_tests.py的方式（重定向输出到devnull，只捕获返回码）
    cmd = [sys.executable, 'pyexz3.py', '-m', '25', '--z3', test_path]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 不重定向输出，查看实际错误
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        print(f"返回码: {process.returncode}")
        
        if process.returncode == 0:
            print("✓ 测试通过")
        else:
            print("✗ 测试失败")
            
            # 检查错误类型
            if stderr:
                print(f"错误输出 (前800字符):")
                print(stderr[:800])
                if len(stderr) > 800:
                    print(f"... (总共{len(stderr)}字符)")
                
                # 分析错误类型
                stderr_lower = stderr.lower()
                if 'import' in stderr_lower and 'error' in stderr_lower:
                    print("错误类型: 导入错误")
                elif 'attribute' in stderr_lower and 'error' in stderr_lower:
                    print("错误类型: 属性错误")
                elif 'type' in stderr_lower and 'error' in stderr_lower:
                    print("错误类型: 类型错误")
                elif 'syntax' in stderr_lower and 'error' in stderr_lower:
                    print("错误类型: 语法错误")
                elif 'z3' in stderr_lower and 'exception' in stderr_lower:
                    print("错误类型: Z3异常")
                elif 'not supported' in stderr_lower or 'unsupported' in stderr_lower:
                    print("错误类型: 不支持的操作")
                elif 'not found' in stderr_lower:
                    print("错误类型: 找不到模块或函数")
                elif 'traceback' in stderr_lower:
                    print("错误类型: Python异常")
                    
            else:
                print("没有错误输出，可能是其他原因失败")
                
            if stdout:
                print(f"标准输出 (前200字符):")
                print(stdout[:200])
                
    except Exception as e:
        print(f"执行异常: {type(e).__name__}: {e}")
        traceback.print_exc()
    
    print("\n" + "-"*40 + "\n")

print("=== 诊断完成 ===")