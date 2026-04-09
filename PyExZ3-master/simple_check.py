#!/usr/bin/env python3
import os, json, sys
from pathlib import Path

def check_week1():
    """检查第一周：稳定函数模式 + 内存级路径树"""
    print("\n=== 第一周：稳定函数模式 + 内存级路径树 ===")
    
    # 检查基础模块
    modules = [
        ('pyexz3.py', '主入口'),
        ('symbolic/loader.py', '加载器'),
        ('symbolic/explore.py', '探索引擎'),
        ('symbolic/invocation.py', '调用器'),
        ('symbolic/path_to_constraint.py', '路径约束'),
        ('symbolic/predicate.py', '谓词'),
        ('symbolic/constraint.py', '约束'),
        ('symbolic/symbolic_types/symbolic_type.py', '符号类型基类'),
        ('symbolic/symbolic_types/symbolic_int.py', '符号整数'),
        ('symbolic/symbolic_types/symbolic_str.py', '符号字符串')
    ]
    
    found = 0
    for path, desc in modules:
        full_path = Path(path)
        exists = full_path.exists()
        status = "OK" if exists else "MISSING"
        print(f"  {desc:15} {status:8} ({path})")
        if exists: found += 1
    
    print(f"  模块存在率: {found}/{len(modules)} ({found/len(modules)*100:.1f}%)")
    return found/len(modules) >= 0.8

def check_week2():
    """检查第二周：可导出 path.json / path.smt2"""
    print("\n=== 第二周：可导出 path.json / path.smt2 ===")
    
    # 检查AST转换和导出模块
    modules = [
        ('symbolic/ast_transform.py', 'AST转换'),
        ('symbolic/runtime_helpers.py', '运行时helper'),
        ('symbolic/trace.py', '轨迹记录'),
        ('symbolic/exporters/json_exporter.py', 'JSON导出器'),
        ('symbolic/exporters/smt_exporter.py', 'SMT导出器'),
        ('symbolic/z3_wrap.py', 'Z3包装器')
    ]
    
    found = 0
    for path, desc in modules:
        full_path = Path(path)
        exists = full_path.exists()
        status = "OK" if exists else "MISSING"
        print(f"  {desc:15} {status:8} ({path})")
        if exists: found += 1
    
    # 检查outputs目录
    outputs_dir = Path("outputs")
    has_outputs = outputs_dir.exists()
    print(f"  outputs目录   {'OK' if has_outputs else 'MISSING':8} (outputs/)")
    
    # 如果存在outputs，检查是否有导出文件
    if has_outputs:
        run_dirs = [d for d in outputs_dir.iterdir() if d.is_dir() and d.name.startswith('run_')]
        if run_dirs:
            latest_run = max(run_dirs, key=lambda x: x.stat().st_mtime)
            files = list(latest_run.iterdir())
            json_files = [f.name for f in files if f.name.endswith('.json')]
            smt_files = [f.name for f in files if f.name.endswith('.smt2')]
            print(f"    最新运行目录: {latest_run.name}")
            print(f"    JSON文件: {json_files}")
            print(f"    SMT2文件: {smt_files}")
    
    return found/len(modules) >= 0.8 and has_outputs

def check_week3():
    """检查第三周：脚本模式 + 语义标签"""
    print("\n=== 第三周：脚本模式 + 语义标签 ===")
    
    # 检查第三周模块
    modules = [
        ('symbolic/script_runner.py', '脚本运行器'),
        ('symbolic/input_model.py', '输入建模'),
        ('symbolic/trace.py', '轨迹记录'),
        ('symbolic/semantic_extractor.py', '语义标签抽取'),
        ('symbolic/normalizer.py', '规范化器'),
        ('test/simple_script.py', '测试脚本')
    ]
    
    found = 0
    for path, desc in modules:
        full_path = Path(path)
        exists = full_path.exists()
        status = "OK" if exists else "MISSING"
        print(f"  {desc:15} {status:8} ({path})")
        if exists: found += 1
    
    # 检查模块内容
    content_checks = []
    
    # 检查script_runner.py是否包含必要方法
    script_runner = Path("symbolic/script_runner.py")
    if script_runner.exists():
        content = script_runner.read_text(encoding='utf-8')
        checks = [
            ('ScriptRunner', 'ScriptRunner类'),
            ('execute_script', 'execute_script方法'),
            ('input()', 'input处理'),
            ('sys.argv', 'argv处理')
        ]
        for key, desc in checks:
            if key in content:
                content_checks.append(f"    ✓ {desc}")
            else:
                content_checks.append(f"    ✗ {desc}")
    
    # 检查input_model.py
    input_model = Path("symbolic/input_model.py")
    if input_model.exists():
        content = input_model.read_text(encoding='utf-8')
        checks = [
            ('InputModel', 'InputModel类'),
            ('InputField', 'InputField类'),
            ('InputType', 'InputType枚举'),
            ('INTEGER', '整数类型'),
            ('STRING', '字符串类型'),
            ('STDIN_LINES', 'stdin_lines类型')
        ]
        for key, desc in checks:
            if key in content:
                content_checks.append(f"    ✓ {desc}")
            else:
                content_checks.append(f"    ✗ {desc}")
    
    if content_checks:
        print("  内容检查:")
        for check in content_checks:
            print(check)
    
    return found/len(modules) >= 0.8

def check_outputs():
    """检查输出目录结构"""
    print("\n=== 输出目录结构检查 ===")
    
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        print("  outputs目录不存在")
        return False
    
    run_dirs = [d for d in outputs_dir.iterdir() if d.is_dir() and d.name.startswith('run_')]
    if not run_dirs:
        print("  没有run_开头的运行目录")
        return False
    
    # 检查最新运行目录
    latest_run = max(run_dirs, key=lambda x: x.stat().st_mtime)
    print(f"  最新运行目录: {latest_run.name}")
    
    files = list(latest_run.iterdir())
    if not files:
        print("  运行目录为空")
        return False
    
    # 统计文件类型
    file_types = {}
    for f in files:
        ext = f.suffix.lower()
        file_types[ext] = file_types.get(ext, 0) + 1
    
    print(f"  文件数量: {len(files)}")
    for ext, count in file_types.items():
        print(f"    {ext or '(无扩展名)'}: {count}个")
    
    # 检查关键文件
    key_files = {
        '.json': 'path.json/trace.json',
        '.smt2': 'path.smt2', 
        '.txt': '日志文件'
    }
    
    for f in files:
        if f.name in ['path.json', 'trace.json', 'semantic_tags.json']:
            size = f.stat().st_size
            print(f"    ✓ {f.name} ({size} bytes)")
        elif f.name == 'path.smt2':
            size = f.stat().st_size
            print(f"    ✓ {f.name} ({size} bytes)")
    
    return len(files) > 0

def main():
    print("=== PyExZ3-master 前三周任务检验 ===")
    print("根据《改进方向.md》要求检查第1-3周完成情况")
    
    # 检查各周
    week1_ok = check_week1()
    week2_ok = check_week2()
    week3_ok = check_week3()
    outputs_ok = check_outputs()
    
    # 总结
    print("\n=== 检验总结 ===")
    weeks = [
        ("第一周", week1_ok, "稳定函数模式 + 内存级路径树"),
        ("第二周", week2_ok, "可导出 path.json / path.smt2"),
        ("第三周", week3_ok, "脚本模式 + 语义标签"),
        ("输出结构", outputs_ok, "输出目录和文件")
    ]
    
    all_ok = True
    for name, ok, desc in weeks:
        status = "✓ 通过" if ok else "✗ 未完成"
        print(f"  {name}: {status} - {desc}")
        if not ok: all_ok = False
    
    print(f"\n总体完成度: {'基本完成' if all_ok else '部分完成，需要改进'}")
    
    if not all_ok:
        print("\n改进建议:")
        if not week1_ok: print("  - 完善第一周基础模块和函数模式")
        if not week2_ok: print("  - 完善AST转换和导出功能")
        if not week3_ok: print("  - 完善脚本模式和语义标签抽取")
        if not outputs_ok: print("  - 运行测试生成输出文件")

if __name__ == "__main__":
    main()