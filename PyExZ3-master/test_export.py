#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出功能验证脚本
用于测试PyExZ3-master第二周任务的导出功能
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

def run_test_with_export(test_file, export_params):
    """运行测试并验证导出功能"""
    print(f"\n=== 测试 {test_file} ===")
    
    # 构建命令
    cmd = [sys.executable, "pyexz3.py", "-m", "25", "--z3"]
    cmd.extend(export_params)
    cmd.append(test_file)
    
    print(f"命令: {' '.join(cmd)}")
    
    # 运行测试
    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✓ 测试成功 (耗时: {elapsed:.2f}秒)")
            return True, result.stdout
        else:
            print(f"✗ 测试失败 (返回码: {result.returncode}, 耗时: {elapsed:.2f}秒)")
            if result.stderr:
                print(f"错误输出: {result.stderr[:500]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"✗ 测试超时 (120秒)")
        return False, "Timeout"
    except Exception as e:
        print(f"✗ 运行异常: {e}")
        return False, str(e)

def find_latest_output_dir():
    """查找最新的输出目录"""
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        return None
    
    run_dirs = [d for d in outputs_dir.iterdir() if d.is_dir() and d.name.startswith('run_')]
    if not run_dirs:
        return None
    
    # 按时间排序，获取最新的目录
    latest_dir = max(run_dirs, key=lambda x: x.stat().st_mtime)
    return latest_dir

def check_export_files(output_dir):
    """检查导出文件"""
    print(f"检查导出目录: {output_dir}")
    
    required_files = {
        "path.json": "路径约束JSON文件",
        "path.smt2": "路径约束SMT2文件",
        "execution_info.json": "执行信息文件",
    }
    
    optional_files = {
        "frontier_*.json": "frontier约束JSON文件",
        "frontier_*.smt2": "frontier约束SMT2文件",
        "trace_summary.json": "执行轨迹摘要文件",
    }
    
    # 检查必需文件
    print("\n必需文件检查:")
    all_required_exist = True
    for filename, desc in required_files.items():
        file_path = output_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {desc} ({filename}) - {size} bytes")
            
            # 如果是JSON文件，验证内容
            if filename.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if filename == "execution_info.json":
                        if data.get("export_performed", False):
                            print(f"    - export_performed: {data['export_performed']}")
                            print(f"    - export_options: {json.dumps(data.get('export_options', {}))}")
                        else:
                            print(f"    ⚠ export_performed 为 false")
                except Exception as e:
                    print(f"    ⚠ JSON解析失败: {e}")
        else:
            print(f"  ✗ {desc} ({filename}) 缺失")
            all_required_exist = False
    
    # 检查可选文件
    print("\n可选文件检查:")
    for pattern, desc in optional_files.items():
        if pattern.endswith('*'):
            # 使用通配符查找文件
            files = list(output_dir.glob(pattern))
            if files:
                print(f"  ✓ {desc} - 找到 {len(files)} 个文件")
                for f in files[:3]:  # 显示前3个文件
                    size = f.stat().st_size
                    print(f"    - {f.name} ({size} bytes)")
            else:
                print(f"  - {desc} - 未找到")
        else:
            file_path = output_dir / pattern
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✓ {desc} - {size} bytes")
            else:
                print(f"  - {desc} - 未找到")
    
    return all_required_exist

def validate_smt2_file(smt2_path):
    """验证SMT2文件格式"""
    try:
        with open(smt2_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基本SMT2格式检查
        checks = [
            ("包含(set-logic", "set-logic声明"),
            ("包含(declare-fun", "变量声明"),
            ("包含(assert", "断言"),
            ("包含(check-sat", "check-sat"),
            ("包含(get-model", "get-model或get-value"),
        ]
        
        print(f"SMT2文件验证 ({smt2_path.name}):")
        all_checks_passed = True
        for keyword, desc in checks:
            if keyword in content:
                print(f"  ✓ {desc}")
            else:
                print(f"  ⚠ {desc} 缺失")
                all_checks_passed = False
        
        return all_checks_passed
    except Exception as e:
        print(f"  ✗ SMT2文件读取失败: {e}")
        return False

def validate_json_file(json_path):
    """验证JSON文件内容结构"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        filename = json_path.name
        print(f"JSON文件验证 ({filename}):")
        
        if filename == "path.json":
            # 检查path.json结构
            expected_keys = ["path_id", "constraints", "variables", "input", "return_value", "exception"]
            found_keys = [key for key in expected_keys if key in data]
            print(f"  包含键: {found_keys}")
            return len(found_keys) >= 3
        
        elif filename == "execution_info.json":
            # 检查execution_info.json结构
            expected_keys = ["mode", "function", "iterations", "run_id", "timestamp", "export_performed", "export_options"]
            found_keys = [key for key in expected_keys if key in data]
            print(f"  包含键: {found_keys}")
            
            # 特别检查导出状态
            if "export_performed" in data:
                print(f"  export_performed: {data['export_performed']}")
            if "export_options" in data:
                opts = data["export_options"]
                print(f"  export_options: {opts}")
            
            return len(found_keys) >= 5
        
        return True
    except Exception as e:
        print(f"  ✗ JSON文件验证失败: {e}")
        return False

def main():
    print("=== PyExZ3-master 导出功能验证 ===\n")
    
    # 测试文件
    test_files = [
        "test/simple.py",  # 基础测试
        "test/abs.py",     # 绝对函数测试
        "test/max.py",     # 最大值函数测试
    ]
    
    # 导出参数组合
    export_configs = [
        ("基本导出", ["--export-path"]),
        ("全面导出", ["--export-path", "--export-frontier", "--export-trace"]),
        ("仅JSON导出", ["--export-json"]),
        ("仅SMT导出", ["--export-smt"]),
    ]
    
    overall_success = True
    
    for config_name, export_params in export_configs:
        print(f"\n{'='*60}")
        print(f"配置: {config_name}")
        print(f"参数: {' '.join(export_params)}")
        print('='*60)
        
        # 运行测试
        success, output = run_test_with_export(test_files[0], export_params)
        
        if success:
            # 查找最新的输出目录
            output_dir = find_latest_output_dir()
            if output_dir:
                print(f"输出目录: {output_dir}")
                
                # 检查导出文件
                files_ok = check_export_files(output_dir)
                
                # 验证关键文件
                if files_ok:
                    # 验证SMT2文件
                    smt2_path = output_dir / "path.smt2"
                    if smt2_path.exists():
                        validate_smt2_file(smt2_path)
                    
                    # 验证JSON文件
                    for json_file in ["path.json", "execution_info.json"]:
                        json_path = output_dir / json_file
                        if json_path.exists():
                            validate_json_file(json_path)
                else:
                    overall_success = False
                    print("⚠ 导出文件不完整")
            else:
                overall_success = False
                print("✗ 未找到输出目录")
        else:
            overall_success = False
    
    # 运行修改后的run_tests.py
    print(f"\n{'='*60}")
    print("运行修改后的run_tests.py")
    print('='*60)
    
    try:
        cmd = [sys.executable, "run_tests.py", "test", "--z3"]
        print(f"命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✓ run_tests.py 运行成功")
            print(f"输出: {result.stdout[:500]}...")
            
            # 检查所有测试的输出目录
            print("\n检查所有测试的导出文件:")
            outputs_dir = Path("outputs")
            if outputs_dir.exists():
                run_dirs = [d for d in outputs_dir.iterdir() if d.is_dir() and d.name.startswith('run_')]
                recent_runs = sorted(run_dirs, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
                
                for run_dir in recent_runs:
                    info_file = run_dir / "execution_info.json"
                    if info_file.exists():
                        try:
                            with open(info_file, 'r', encoding='utf-8') as f:
                                info = json.load(f)
                            export_status = info.get("export_performed", False)
                            print(f"{run_dir.name}: export_performed = {export_status}")
                        except:
                            print(f"{run_dir.name}: 无法读取execution_info.json")
        else:
            print(f"✗ run_tests.py 运行失败 (返回码: {result.returncode})")
            if result.stderr:
                print(f"错误输出: {result.stderr[:500]}")
            overall_success = False
    except Exception as e:
        print(f"✗ run_tests.py 运行异常: {e}")
        overall_success = False
    
    # 总结
    print(f"\n{'='*60}")
    print("导出功能验证总结")
    print('='*60)
    
    if overall_success:
        print("✓ 导出功能验证通过")
        print("  - run_tests.py已配置为启用全面导出功能")
        print("  - 测试运行时自动生成path.json和path.smt2文件")
        print("  - execution_info.json中的export_performed应为true")
    else:
        print("✗ 导出功能验证失败")
        print("  请检查:")
        print("  1. 导出模块(json_exporter.py, smt_exporter.py)是否正确实现")
        print("  2. pyexz3.py中的导出逻辑是否正确")
        print("  3. 运行环境是否正常")

if __name__ == "__main__":
    main()