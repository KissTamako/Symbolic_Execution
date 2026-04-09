#!/usr/bin/env python
"""
验证z3_wrap.py的SMT导出功能
"""
import os
import sys
import tempfile
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("=== 验证z3_wrap.py导出功能 ===")
print(f"当前目录: {os.getcwd()}")

# 1. 检查Z3Wrapper类的导出方法
print("\n--- 检查Z3Wrapper导出方法 ---")
try:
    from symbolic.z3_wrap import Z3Wrapper
    
    # 创建Z3Wrapper实例
    wrapper = Z3Wrapper()
    
    # 检查方法是否存在
    methods = ['build_solver', 'export_current_query_to_smt2', 'export_constraints_to_smt2']
    for method in methods:
        if hasattr(wrapper, method):
            print(f"[OK] Z3Wrapper.{method} 方法存在")
        else:
            print(f"[ERROR] Z3Wrapper.{method} 方法不存在")
            
except Exception as e:
    print(f"[ERROR] 导入Z3Wrapper失败: {e}")
    import traceback
    traceback.print_exc()

# 2. 创建测试约束并导出SMT2
print("\n--- 测试SMT2导出功能 ---")
try:
    from symbolic.z3_wrap import Z3Wrapper
    from symbolic.predicate import Predicate
    
    # 创建简单的测试约束
    # 我们需要创建一些断言
    wrapper = Z3Wrapper()
    
    # 尝试创建简单的断言
    # 注意：这里简化处理，实际使用可能需要更复杂的断言对象
    test_asserts = []  # 空断言列表
    test_query = None   # 空查询
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.smt2', delete=False) as tmp:
        tmp_path = tmp.name
    
    print(f"临时文件: {tmp_path}")
    
    # 测试export_constraints_to_smt2
    result = wrapper.export_constraints_to_smt2(
        asserts=test_asserts,
        query=test_query,
        output_path=tmp_path,
        negate_query=True,
        solver_logic="QF_LIA"
    )
    
    if result is not None:
        print(f"[OK] export_constraints_to_smt2 成功，文件: {result}")
        
        # 检查文件内容
        if os.path.exists(tmp_path):
            with open(tmp_path, 'r') as f:
                content = f.read()
                print(f"文件大小: {len(content)} 字符")
                print("文件前几行:")
                for i, line in enumerate(content.split('\n')[:10]):
                    if line.strip():
                        print(f"  {i+1}: {line[:80]}")
        else:
            print("[WARN] 导出的文件不存在")
    else:
        print("[WARN] export_constraints_to_smt2 返回 None")
        
    # 清理临时文件
    try:
        os.unlink(tmp_path)
    except:
        pass
        
except Exception as e:
    print(f"[ERROR] SMT2导出测试失败: {e}")
    import traceback
    traceback.print_exc()

# 3. 检查相关的导出模块
print("\n--- 检查导出模块 ---")
exporters_dir = 'symbolic/exporters'
if os.path.exists(exporters_dir):
    print(f"[OK] 导出器目录存在: {exporters_dir}")
    
    # 列出文件
    for file in os.listdir(exporters_dir):
        if file.endswith('.py') and not file.startswith('__'):
            print(f"  - {file}")
else:
    print(f"[WARN] 导出器目录不存在: {exporters_dir}")

# 检查smt_exporter.py
smt_exporter_path = 'symbolic/exporters/smt_exporter.py'
if os.path.exists(smt_exporter_path):
    print(f"[OK] smt_exporter.py 存在")
    
    # 检查关键类
    try:
        from symbolic.exporters.smt_exporter import SMTExporter
        print(f"[OK] SMTExporter 类可导入")
    except Exception as e:
        print(f"[WARN] 导入SMTExporter失败: {e}")
else:
    print(f"[WARN] smt_exporter.py 不存在")

# 4. 检查pyexz3.py中的导出选项
print("\n--- 检查命令行导出选项 ---")
try:
    import symbolic.loader  # 确保模块可导入
    
    # 检查pyexz3.py中的导出参数
    pyexz3_path = 'pyexz3.py'
    if os.path.exists(pyexz3_path):
        with open(pyexz3_path, 'r') as f:
            content = f.read()
            
        export_flags = [
            '--export-smt',
            '--export-json', 
            '--export-path',
            '--export-frontier',
            '--export-trace'
        ]
        
        for flag in export_flags:
            if flag in content:
                print(f"[OK] 命令行参数 {flag} 存在")
            else:
                print(f"[WARN] 命令行参数 {flag} 不存在")
    else:
        print("[ERROR] pyexz3.py 不存在")
        
except Exception as e:
    print(f"[ERROR] 检查命令行选项失败: {e}")

print("\n=== 验证完成 ===")