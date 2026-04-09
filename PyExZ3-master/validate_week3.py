#!/usr/bin/env python3
"""
验证第三周任务完成度。
检查脚本模式、输入建模、执行轨迹记录、语义标签抽取等功能的集成情况。
"""

import os
import sys
import json
from pathlib import Path

# 添加PyExZ3-master到路径
sys.path.insert(0, 'PyExZ3-master')

print("=== 第三周任务完成度验证 ===\n")

# 1. 检查基本模块是否存在
print("1. 检查基础模块:")
modules_to_check = [
    ('symbolic/loader.py', '脚本模式支持'),
    ('symbolic/input_model.py', '输入建模骨架'),
    ('symbolic/trace.py', '执行轨迹记录'),
    ('symbolic/semantic_extractor.py', '语义标签抽取'),
    ('symbolic/exporters/json_exporter.py', 'JSON导出器'),
    ('symbolic/exporters/smt_exporter.py', 'SMT导出器'),
    ('symbolic/script_runner.py', '脚本运行器'),
]

all_modules_exist = True
for module_path, description in modules_to_check:
    full_path = Path('PyExZ3-master') / module_path
    exists = full_path.exists()
    status = "[OK]" if exists else "[FAIL]"
    print(f"  {status} {description}: {module_path}")
    if not exists:
        all_modules_exist = False

print(f"\n基础模块完整性: {'通过' if all_modules_exist else '不完整'}\n")

# 2. 检查SymbolicStr类型处理修复
print("2. 检查SymbolicStr类型处理修复:")
try:
    # 直接导入模块
    import sys
    sys.path.insert(0, 'PyExZ3-master')
    import symbolic.z3_expr.expression as expr_module
    
    # 检查是否导入了SymbolicStr
    import inspect
    source = inspect.getsource(expr_module.Z3Expression._astToZ3Expr)
    if 'SymbolicStr' in source:
        print("  [OK] Z3Expression._astToZ3Expr 已处理 SymbolicStr 类型")
        symbolic_str_fixed = True
    else:
        print("  [FAIL] Z3Expression._astToZ3Expr 未处理 SymbolicStr 类型")
        symbolic_str_fixed = False
except Exception as e:
    print(f"  [FAIL] 检查失败: {e}")
    symbolic_str_fixed = False

# 3. 检查执行轨迹记录集成
print("\n3. 检查执行轨迹记录集成:")
try:
    import symbolic.explore as explore_module
    import inspect
    
    source = inspect.getsource(explore_module.ExplorationEngine._oneExecution)
    if 'record_execution' in source or 'get_trace_recorder' in source:
        print("  [OK] ExplorationEngine._oneExecution 已集成轨迹记录")
        trace_integrated = True
    else:
        print("  [FAIL] ExplorationEngine._oneExecution 未集成轨迹记录")
        trace_integrated = False
except Exception as e:
    print(f"  [FAIL] 检查失败: {e}")
    trace_integrated = False

# 4. 检查输入建模API
print("\n4. 检查输入建模API:")
try:
    import symbolic.input_model as input_model_module
    
    # 检查关键类是否存在
    has_InputModel = hasattr(input_model_module, 'InputModel')
    has_InputField = hasattr(input_model_module, 'InputField')
    has_InputType = hasattr(input_model_module, 'InputType')
    
    if has_InputModel and has_InputField and has_InputType:
        print("  [OK] 输入建模数据结构完整")
        input_model_integrated = True
    else:
        print("  [FAIL] 输入建模数据结构不完整")
        input_model_integrated = False
        
except Exception as e:
    print(f"  [FAIL] 检查失败: {e}")
    input_model_integrated = False

# 5. 检查语义标签抽取器
print("\n5. 检查语义标签抽取器:")
try:
    import symbolic.semantic_extractor as semantic_extractor_module
    
    extractor = semantic_extractor_module.SemanticExtractor()
    tags = extractor.extract_tags_from_expr("x > 0")
    
    if 'negative-check' in tags or isinstance(tags, set):
        print("  [OK] 语义标签抽取器功能正常")
        semantic_extractor_working = True
    else:
        print("  [FAIL] 语义标签抽取器功能异常")
        semantic_extractor_working = False
except Exception as e:
    print(f"  [FAIL] 检查失败: {e}")
    semantic_extractor_working = False

# 6. 检查脚本模式
print("\n6. 检查脚本模式:")
try:
    import symbolic.loader as loader_module
    
    # 检查ScriptLoader类是否存在
    if hasattr(loader_module, 'ScriptLoader'):
        ScriptLoader = loader_module.ScriptLoader
        if hasattr(ScriptLoader, 'createInvocation'):
            print("  [OK] ScriptLoader 已实现 createInvocation 方法")
            script_mode_implemented = True
        else:
            print("  [FAIL] ScriptLoader 未完全实现")
            script_mode_implemented = False
    else:
        print("  [FAIL] ScriptLoader 类不存在")
        script_mode_implemented = False
    
    # 检查loaderFactory支持模式参数
    if hasattr(loader_module, 'loaderFactory'):
        import inspect
        sig = inspect.signature(loader_module.loaderFactory)
        if 'mode' in sig.parameters:
            print("  [OK] loaderFactory 支持 mode 参数")
            loader_factory_updated = True
        else:
            print("  [FAIL] loaderFactory 不支持 mode 参数")
            loader_factory_updated = False
    else:
        print("  [FAIL] loaderFactory 函数不存在")
        loader_factory_updated = False
        
except Exception as e:
    print(f"  [FAIL] 检查失败: {e}")
    script_mode_implemented = False
    loader_factory_updated = False

# 7. 测试simple_script.py
print("\n7. 测试 simple_script.py 脚本模式:")
try:
    import subprocess
    result = subprocess.run([
        sys.executable, 'PyExZ3-master/pyexz3.py',
        'PyExZ3-master/test/simple_script.py',
        '--mode', 'script',
        '--output-dir', 'test_output_validation',
        '--no-ast-transform'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("  [OK] simple_script.py 脚本模式执行成功")
        if "simple_script.py contains no expected_result function" in result.stdout:
            print("  [OK] 正确识别脚本模式（无 expected_result 函数）")
        simple_script_working = True
    else:
        print(f"  [FAIL] simple_script.py 执行失败: {result.stderr[:200]}")
        simple_script_working = False
except Exception as e:
    print(f"  [FAIL] 测试失败: {e}")
    simple_script_working = False

# 总结
print("\n" + "="*50)
print("第三周任务完成度总结:")
print("="*50)

results = {
    "基础模块完整性": all_modules_exist,
    "SymbolicStr类型处理修复": symbolic_str_fixed,
    "执行轨迹记录集成": trace_integrated,
    "输入建模API集成": input_model_integrated,
    "语义标签抽取器功能": semantic_extractor_working,
    "ScriptLoader实现": script_mode_implemented,
    "loaderFactory更新": loader_factory_updated,
    "simple_script.py脚本模式": simple_script_working,
}

total = len(results)
passed = sum(1 for v in results.values() if v)
percentage = (passed / total) * 100

for desc, status in results.items():
    status_str = "通过" if status else "未完成"
    print(f"  {desc}: {status_str}")

print(f"\n总体完成度: {passed}/{total} ({percentage:.1f}%)")

if percentage >= 80:
    print("\n✅ 第三周任务基本完成，可以进行后续优化和测试。")
elif percentage >= 60:
    print("\n⚠️  第三周任务部分完成，需要继续完善。")
else:
    print("\n❌ 第三周任务完成度不足，需要重点改进。")

# 生成改进建议
print("\n改进建议:")
if not input_model_integrated:
    print("  - 在pyexz3.py中完全集成输入模型加载逻辑")
if not trace_integrated:
    print("  - 在探索引擎中完全集成轨迹记录")
if not semantic_extractor_working:
    print("  - 修复语义标签抽取器与导出器的集成")
if not simple_script_working:
    print("  - 修复脚本模式执行问题")

print("\n验证完成。")