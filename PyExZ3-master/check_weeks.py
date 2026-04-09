#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyExZ3-master 前三周任务全面检验
根据《改进方向.md》要求，检查第1-3周任务完成情况
"""

import sys
import os
import json
import subprocess
import traceback
from pathlib import Path

def main():
    print("=== PyExZ3-master 前三周任务全面检验 ===")
    print("根据《改进方向.md》要求，检查第1-3周任务完成情况\n")
    
    # ============================================
    # 1. 第一周任务检验：稳定函数模式 + 内存级路径树
    # ============================================
    print("=== 第一周：稳定函数模式 + 内存级路径树 ===")
    
    # 1.1 检查入口与配置
    print("1. 入口与配置检查:")
    pyexz3_path = "pyexz3.py"
    if os.path.exists(pyexz3_path):
        with open(pyexz3_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = {
            "--mode=": "支持mode参数",
            "--dump-constraints": "支持dump-constraints",
            "--dump-trace": "支持dump-trace", 
            "--dump-semantics": "支持dump-semantics",
            "outputs/": "输出目录结构约定"
        }
        
        for key, desc in checks.items():
            if key in content:
                print(f"   ✓ {desc}")
            else:
                print(f"   ✗ {desc} 缺失")
    else:
        print("   ✗ pyexz3.py 不存在")
    
    # 1.2 检查模块骨架
    print("\n2. 模块骨架检查:")
    week1_modules = [
        "symbolic/exporters/",
        "symbolic/runtime_helpers.py",
        "symbolic/trace.py", 
        "symbolic/semantic_extractor.py",
        "symbolic/input_model.py",
        "symbolic/script_runner.py"
    ]
    
    for module in week1_modules:
        if os.path.exists(module):
            print(f"   ✓ {module}")
        else:
            print(f"   ✗ {module} 缺失")
    
    # 1.3 检查执行主循环
    print("\n3. 执行主循环检查:")
    try:
        # 尝试导入关键模块
        sys.path.insert(0, os.getcwd())
        import symbolic.explore
        import symbolic.loader
        import symbolic.invocation
        
        print("   ✓ explore.py 导入成功")
        print("   ✓ loader.py 导入成功") 
        print("   ✓ invocation.py 导入成功")
        
        # 检查函数模式
        if hasattr(symbolic.loader, "Loader"):
            print("   ✓ Loader类存在")
        if hasattr(symbolic.loader, "create_function_invocation") or hasattr(symbolic.loader, "loaderFactory"):
            print("   ✓ 函数模式支持")
            
    except Exception as e:
        print(f"   ✗ 模块导入失败: {e}")
    
    # 1.4 检查路径约束主干
    print("\n4. 路径约束主干检查:")
    try:
        import symbolic.path_to_constraint
        
        # 检查Predicate结构
        import symbolic.predicate as pred_module
        if hasattr(pred_module, "Predicate"):
            Predicate = pred_module.Predicate
            # 检查字段
            import inspect
            sig = inspect.signature(Predicate.__init__)
            params = list(sig.parameters.keys())
            
            expected_fields = ["expr", "result", "source_file", "source_line", "branch_id", "vars"]
            found = 0
            for field in expected_fields:
                if field in str(sig):
                    found += 1
                    print(f"   ✓ Predicate有{field}字段")
            
            if found >= 4:
                print(f"   ✓ Predicate基本结构化字段完整 ({found}/6)")
            else:
                print(f"   ✗ Predicate字段不完整 ({found}/6)")
                
        # 检查Constraint方法
        import symbolic.constraint as const_module
        if hasattr(const_module, "Constraint"):
            Constraint = const_module.Constraint
            if hasattr(Constraint, "to_dict") or hasattr(Constraint, "get_path_predicates"):
                print("   ✓ Constraint有to_dict或get_path_predicates方法")
                
    except Exception as e:
        print(f"   ✗ 路径约束检查失败: {e}")
    
    # 1.5 检查符号对象基线
    print("\n5. 符号对象基线检查:")
    try:
        import symbolic.symbolic_types.symbolic_type
        import symbolic.symbolic_types.symbolic_int
        import symbolic.symbolic_types.symbolic_str
        
        print("   ✓ symbolic_type.py 导入成功")
        print("   ✓ symbolic_int.py 导入成功")
        print("   ✓ symbolic_str.py 导入成功")
        
        # 检查bool/int/str支持
        from symbolic.symbolic_types import SymbolicInteger, SymbolicString, SymbolicBool
        print("   ✓ SymbolicInteger 类存在")
        print("   ✓ SymbolicString 类存在")
        print("   ✓ SymbolicBool 类存在")
        
    except Exception as e:
        print(f"   ✗ 符号对象检查失败: {e}")
    
    # ============================================
    # 2. 第二周任务检验：可导出 path.json / path.smt2
    # ============================================
    print("\n\n=== 第二周：可导出 path.json / path.smt2 ===")
    
    # 2.1 检查AST转换
    print("1. AST转换检查:")
    ast_transform_path = "symbolic/ast_transform.py"
    if os.path.exists(ast_transform_path):
        with open(ast_transform_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        ast_checks = {
            "transform_ast": "transform_ast函数",
            "_se_int": "_se_int调用",
            "_se_str": "_se_str调用", 
            "_se_range": "_se_range调用",
            "wrap_concrete_constant": "常量包装"
        }
        
        for key, desc in ast_checks.items():
            if key in content:
                print(f"   ✓ {desc}")
            else:
                print(f"   ✗ {desc} 缺失")
    else:
        print("   ✗ ast_transform.py 不存在")
    
    # 2.2 检查运行时helper
    print("\n2. 运行时helper检查:")
    runtime_helpers_path = "symbolic/runtime_helpers.py"
    if os.path.exists(runtime_helpers_path):
        with open(runtime_helpers_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        helper_checks = [
            "_se_int",
            "_se_str", 
            "_se_range",
            "unwrap",
            "wrap_concrete_constant"
        ]
        
        for helper in helper_checks:
            if helper in content:
                print(f"   ✓ {helper} 函数")
            else:
                print(f"   ✗ {helper} 缺失")
    else:
        print("   ✗ runtime_helpers.py 不存在")
    
    # 2.3 检查分支位置信息
    print("\n3. 分支位置信息检查:")
    try:
        import symbolic.trace
        
        # 检查branch hook
        if "branch_hook" in content or "branch" in content.lower():
            print("   ✓ 分支hook相关代码存在")
        
        # 检查trace模块
        if hasattr(symbolic.trace, "TraceRecorder"):
            print("   ✓ TraceRecorder类存在")
            
    except Exception as e:
        print(f"   ✗ 分支位置检查失败: {e}")
    
    # 2.4 检查SMT与JSON导出
    print("\n4. SMT与JSON导出检查:")
    exporters_dir = "symbolic/exporters"
    if os.path.exists(exporters_dir):
        exporter_files = os.listdir(exporters_dir)
        print(f"   ✓ exporters目录存在，包含文件: {exporter_files}")
        
        # 检查具体文件
        if "json_exporter.py" in exporter_files:
            json_exp_path = os.path.join(exporters_dir, "json_exporter.py")
            with open(json_exp_path, "r", encoding="utf-8") as f:
                json_content = f.read()
            
            if "JSONExporter" in json_content or "export" in json_content.lower():
                print("   ✓ json_exporter.py 有导出功能")
        
        if "smt_exporter.py" in exporter_files:
            smt_exp_path = os.path.join(exporters_dir, "smt_exporter.py")
            with open(smt_exp_path, "r", encoding="utf-8") as f:
                smt_content = f.read()
            
            if "SMTExporter" in smt_content or "smt" in smt_content.lower():
                print("   ✓ smt_exporter.py 有SMT导出功能")
    else:
        print("   ✗ exporters目录不存在")
    
    # 2.5 检查Z3Wrapper
    print("\n5. Z3Wrapper检查:")
    z3_wrap_path = "symbolic/z3_wrap.py"
    if os.path.exists(z3_wrap_path):
        with open(z3_wrap_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "Z3Wrapper" in content:
            print("   ✓ Z3Wrapper类存在")
        
        z3_checks = [
            "build_solver",
            "export_current_query_to_smt2",
            "to_smt2"
        ]
        
        for check in z3_checks:
            if check in content:
                print(f"   ✓ {check} 方法存在")
    else:
        print("   ✗ z3_wrap.py 不存在")
    
    # ============================================
    # 3. 第三周任务检验：脚本模式 + 语义标签
    # ============================================
    print("\n\n=== 第三周：脚本模式 + 语义标签 ===")
    
    # 3.1 检查脚本模式执行
    print("1. 脚本模式执行检查:")
    script_runner_path = "symbolic/script_runner.py"
    if os.path.exists(script_runner_path):
        with open(script_runner_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        script_checks = {
            "ScriptRunner": "ScriptRunner类",
            "create_script_invocation": "创建脚本调用",
            "execute_script": "执行脚本方法",
            "input()": "input()处理",
            "sys.argv": "sys.argv处理"
        }
        
        for key, desc in script_checks.items():
            if key in content:
                print(f"   ✓ {desc}")
            else:
                print(f"   ✗ {desc} 缺失")
    else:
        print("   ✗ script_runner.py 不存在")
    
    # 3.2 检查输入建模
    print("\n2. 输入建模检查:")
    input_model_path = "symbolic/input_model.py"
    if os.path.exists(input_model_path):
        with open(input_model_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        input_checks = {
            "InputModel": "InputModel类",
            "InputField": "InputField类",
            "InputType": "InputType枚举",
            "INTEGER": "整数类型",
            "STRING": "字符串类型",
            "STDIN_LINES": "stdin_lines类型",
            "ARGV": "argv类型",
            "min_value": "最小值约束",
            "max_value": "最大值约束",
            "max_length": "最大长度约束"
        }
        
        for key, desc in input_checks.items():
            if key in content:
                print(f"   ✓ {desc}")
            else:
                print(f"   ✗ {desc} 缺失")
    else:
        print("   ✗ input_model.py 不存在")
    
    # 3.3 检查执行轨迹
    print("\n3. 执行轨迹检查:")
    trace_path = "symbolic/trace.py"
    if os.path.exists(trace_path):
        with open(trace_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        trace_checks = {
            "TraceRecorder": "TraceRecorder类",
            "record_execution": "record_execution函数",
            "concrete_inputs": "记录具体输入",
            "return_value": "记录返回值",
            "exception": "记录异常",
            "branch_trace": "记录分支轨迹",
            "path_id": "记录路径ID"
        }
        
        for key, desc in trace_checks.items():
            if key in content:
                print(f"   ✓ {desc}")
            else:
                print(f"   ✗ {desc} 缺失")
    else:
        print("   ✗ trace.py 不存在")
    
    # 3.4 检查语义标签抽取
    print("\n4. 语义标签抽取检查:")
    semantic_path = "symbolic/semantic_extractor.py"
    if os.path.exists(semantic_path):
        with open(semantic_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        semantic_checks = [
            "SemanticExtractor",
            "negative-check",
            "zero-check", 
            "empty-string-check",
            "length-bound-check",
            "contains-check",
            "prefix-check",
            "suffix-check",
            "exception-path",
            "division-by-zero-risk",
            "index-out-of-range-risk"
        ]
        
        for check in semantic_checks:
            if check in content:
                print(f"   ✓ {check}")
            else:
                print(f"   ✗ {check} 缺失")
    else:
        print("   ✗ semantic_extractor.py 不存在")
    
    # 3.5 检查结果解释
    print("\n5. 结果解释检查:")
    normalizer_path = "symbolic/normalizer.py"
    if os.path.exists(normalizer_path):
        with open(normalizer_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "Normalizer" in content:
            print("   ✓ Normalizer类存在")
        if "normalize_expression" in content:
            print("   ✓ normalize_expression函数存在")
        if "execution_summary" in content.lower():
            print("   ✓ execution_summary相关功能")
    else:
        print("   ✗ normalizer.py 不存在")
    
    # ============================================
    # 4. 输出目录和文件结构检验
    # ============================================
    print("\n\n=== 输出目录和文件结构检验 ===")
    
    # 检查outputs目录
    outputs_dir = "outputs"
    if os.path.exists(outputs_dir):
        print(f"1. outputs目录存在")
        
        # 查找最新的run目录
        run_dirs = [d for d in os.listdir(outputs_dir) if d.startswith("run_")]
        if run_dirs:
            latest_run = max(run_dirs, key=lambda x: os.path.getmtime(os.path.join(outputs_dir, x)))
            latest_path = os.path.join(outputs_dir, latest_run)
            print(f"   最新运行目录: {latest_run}")
            
            # 检查目录内容
            files = os.listdir(latest_path)
            print(f"   目录内容: {files}")
            
            # 检查关键文件
            key_files = {
                "path.json": "路径JSON文件",
                "path.smt2": "路径SMT2文件",
                "trace.json": "轨迹文件",
                "semantic_tags.json": "语义标签文件"
            }
            
            for file, desc in key_files.items():
                if file in files:
                    file_path = os.path.join(latest_path, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   ✓ {desc} 存在 ({file_size} bytes)")
                    
                    # 如果是JSON文件，可以检查内容结构
                    if file.endswith(".json"):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                            if isinstance(data, dict) and len(data) > 0:
                                print(f"     JSON结构有效，包含键: {list(data.keys())[:5]}...")
                        except:
                            print(f"     JSON解析失败")
                else:
                    print(f"   ✗ {desc} 缺失")
        else:
            print("   ✗ 没有run_开头的目录")
    else:
        print("1. outputs目录不存在，可能需要运行一次符号执行")
    
    # ============================================
    # 5. 运行简单测试验证功能
    # ============================================
    print("\n\n=== 功能运行验证 ===")
    
    print("1. 运行simple_script.py测试...")
    try:
        # 使用subprocess运行符号执行
        cmd = [sys.executable, "pyexz3.py", "-m", "3", "--z3", "test/simple_script.py"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✓ simple_script.py 运行成功")
            
            # 检查输出是否包含成功信息
            if "Exploration completed successfully" in result.stdout or "completed" in result.stdout.lower():
                print("   ✓ 探索完成成功信息")
            
            # 检查是否提到了路径
            if "path" in result.stdout.lower():
                print("   ✓ 输出包含路径信息")
                
            # 检查是否有错误
            if "error" in result.stdout.lower() or "Error" in result.stdout:
                print("   ⚠ 输出包含错误信息")
        else:
            print(f"   ✗ 运行失败，返回码: {result.returncode}")
            print(f"     错误输出: {result.stderr[:200]}")
            
    except subprocess.TimeoutExpired:
        print("   ✗ 运行超时")
    except Exception as e:
        print(f"   ✗ 运行异常: {e}")
    
    print("\n2. 检查测试通过率...")
    test_script = "run_tests.py"
    if os.path.exists(test_script):
        try:
            # 运行简单测试检查
            cmd = [sys.executable, test_script, "--list"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("   ✓ run_tests.py 可执行")
                # 粗略检查测试输出
                if "test" in result.stdout.lower():
                    print("   ✓ 测试列表输出正常")
        except:
            print("   ⚠ 测试检查跳过")
    
    print("\n=== 检验完成 ===")
    print("\n注：以上检验基于文件存在性和代码结构分析。")
    print("    实际功能完整性需要运行具体测试验证。")

if __name__ == "__main__":
    main()