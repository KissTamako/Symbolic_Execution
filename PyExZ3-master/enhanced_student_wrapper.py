#!/usr/bin/env python3
"""
增强型学生代码自动包装器 V2

自动将学生代码转换为可分析的函数形式，支持：
1. 全面的输入检测和处理（input、文件、网络、sys.stdin等）
2. 增强的输出处理（print、文件、返回值等）
3. 特殊函数的安全包装（eval、exec、open、random等）
4. 控制流分析和处理（try/except、循环、嵌套等）
5. 边界条件检测和处理（零除、数组越界，空值等）
"""

import ast
import argparse
import sys
import os
import random
import time
from typing import Optional, List, Tuple, Dict, Any, Set
from enum import Enum


class InputType(Enum):
    """输入类型枚举"""
    INTERACTIVE = "interactive"
    FILE = "file"
    STDIN = "stdin"
    NETWORK = "network"
    RANDOM = "random"
    CONSTANT = "constant"
    INFERRED = "inferred"


class OutputType(Enum):
    """输出类型枚举"""
    PRINT = "print"
    FILE = "file"
    RETURN = "return"
    STDERR = "stderr"


class SpecialFunction(Enum):
    """特殊函数类型枚举"""
    EVAL = "eval"
    EXEC = "exec"
    OPEN = "open"
    RANDOM = "random"
    TIME = "time"
    SYS_STDIN = "sys.stdin"
    SYS_STDOUT = "sys.stdout"
    SYS_STDERR = "sys.stderr"


class EnhancedAnalyzer(ast.NodeVisitor):
    """增强型学生代码分析器"""

    def __init__(self):
        # 基本信息
        self.functions = []
        self.global_vars = []
        self.import_statements = []
        self.has_main = False

        # 输入分析
        self.input_calls = []
        self.input_chained_calls = []  # 链式调用，如 input().split()
        self.file_input_sites = []
        self.stdin_sites = []
        self.random_calls = []
        self.inferred_inputs = []

        # 输出分析
        self.print_calls = []
        self.file_output_sites = []
        self.return_statements = []
        self.stderr_sites = []

        # 特殊函数分析
        self.eval_calls = []
        self.exec_calls = []
        self.open_calls = []
        self.time_calls = []
        self.compile_calls = []  # compile() 调用

        # 控制流分析
        self.try_except_blocks = []
        self.loop_structures = []
        self.conditional_structures = []
        self.nested_depth = 0
        self.max_nested_depth = 0

        # 高级语言特性
        self.lambda_count = 0  # lambda 表达式数量
        self.yield_count = 0  # yield 语句数量
        self.async_count = 0  # 异步函数数量

        # 边界条件分析
        self.division_ops = []
        self.subscript_ops = []
        self.subscript_targets = {}
        self.comparisons = []

        # 代码语句
        self.top_level_code = []

    def analyze(self, code: str) -> Dict[str, Any]:
        """分析学生代码"""
        try:
            tree = ast.parse(code)
            # 设置父节点链接
            self._set_parents(tree)
            self.visit(tree)
            return self.get_analysis_result()
        except SyntaxError as e:
            return {"error": f"语法错误: {e}", "success": False}

    def _set_parents(self, node, parent=None):
        """递归设置所有节点的父节点"""
        for child in ast.iter_child_nodes(node):
            child._parent = parent
            self._set_parents(child, child)

    def get_analysis_result(self) -> Dict[str, Any]:
        """获取分析结果"""
        return {
            "success": True,
            "functions": self.functions,
            "global_vars": self.global_vars,
            "import_statements": self.import_statements,
            "has_main": self.has_main,
            "inputs": self._summarize_inputs(),
            "outputs": self._summarize_outputs(),
            "special_functions": self._summarize_special_functions(),
            "control_flow": self._summarize_control_flow(),
            "boundary_conditions": self._summarize_boundary_conditions(),
            "complexity_score": self._calculate_complexity_score(),
            "warnings": self._generate_warnings(),
        }

    def _summarize_inputs(self) -> Dict[str, Any]:
        """汇总输入信息"""
        return {
            "interactive_count": len(self.input_calls),
            "chained_input_count": len(self.input_chained_calls),
            "file_input_count": len(self.file_input_sites),
            "stdin_count": len(self.stdin_sites),
            "random_count": len(self.random_calls),
            "total_input_sites": len(self.input_calls) + len(self.file_input_sites) + len(self.stdin_sites),
            "needs_input_model": len(self.input_calls) + len(self.file_input_sites) + len(self.stdin_sites) > 0,
            "input_details": self.input_calls,
        }

    def _summarize_outputs(self) -> Dict[str, Any]:
        """汇总输出信息"""
        return {
            "print_count": len(self.print_calls),
            "file_output_count": len(self.file_output_sites),
            "return_count": len(self.return_statements),
            "stderr_count": len(self.stderr_sites),
            "output_details": {
                "prints": self.print_calls,
                "returns": len(self.return_statements) > 0,
            },
        }

    def _summarize_special_functions(self) -> Dict[str, Any]:
        """汇总特殊函数信息"""
        return {
            "eval_count": len(self.eval_calls),
            "exec_count": len(self.exec_calls),
            "open_count": len(self.open_calls),
            "time_count": len(self.time_calls),
            "random_count": len(self.random_calls),
            "has_dangerous_functions": len(self.eval_calls) > 0 or len(self.exec_calls) > 0,
            "needs_safe_wrappers": len(self.eval_calls) > 0 or len(self.exec_calls) > 0 or len(self.open_calls) > 0,
        }

    def _summarize_control_flow(self) -> Dict[str, Any]:
        """汇总控制流信息"""
        return {
            "try_except_count": len(self.try_except_blocks),
            "loop_count": len(self.loop_structures),
            "conditional_count": len(self.conditional_structures),
            "max_nested_depth": self.max_nested_depth,
            "has_exception_handling": len(self.try_except_blocks) > 0,
            "has_loops": len(self.loop_structures) > 0,
        }

    def _summarize_boundary_conditions(self) -> Dict[str, Any]:
        """汇总边界条件信息"""
        return {
            "division_count": len(self.division_ops),
            "subscript_count": len(self.subscript_ops),
            "comparison_count": len(self.comparisons),
            "needs_division_check": len(self.division_ops) > 0,
            "needs_bounds_check": len(self.subscript_ops) > 0,
        }

    def _calculate_complexity_score(self) -> int:
        """计算代码复杂度分数"""
        score = 0
        score += len(self.functions) * 2
        score += len(self.input_calls)
        score += len(self.print_calls)
        score += len(self.loop_structures) * 3
        score += len(self.try_except_blocks) * 2
        score += self.max_nested_depth * 2
        score += len(self.division_ops) * 2
        score += len(self.subscript_ops) * 2
        return score

    def _generate_warnings(self) -> List[str]:
        """生成警告信息"""
        warnings = []

        if len(self.eval_calls) > 0:
            warnings.append("代码包含 eval() 调用，可能存在安全风险")

        if len(self.exec_calls) > 0:
            warnings.append("代码包含 exec() 调用，可能存在安全风险")

        if len(self.division_ops) > 0:
            warnings.append("代码包含除法操作，需要检查零除情况")

        if len(self.subscript_ops) > 0:
            warnings.append("代码包含索引操作，需要检查数组越界情况")

        if self.max_nested_depth > 5:
            warnings.append(f"代码嵌套深度较大 ({self.max_nested_depth})，可能导致符号执行复杂度增加")

        if len(self.loop_structures) > 0:
            warnings.append("代码包含循环结构，符号执行可能需要较多迭代")

        if not self.return_statements and len(self.print_calls) == 0:
            warnings.append("代码没有明确的输出，可能无法验证执行结果")

        # 添加对不支持功能的警告
        if self.lambda_count > 0:
            warnings.append(f"代码包含 {self.lambda_count} 个 lambda 表达式，包装器可能无法正确处理")

        if self.yield_count > 0:
            warnings.append(f"代码包含 {self.yield_count} 个 yield 语句，生成器可能被错误处理")

        if len(self.compile_calls) > 0:
            warnings.append(f"代码包含 {len(self.compile_calls)} 个 compile() 调用，动态代码执行不被支持")

        if self.async_count > 0:
            warnings.append(f"代码包含 {self.async_count} 个异步函数，异步功能不被支持")

        return warnings

    def _check_call_function(self, call_node, line_no, context=None):
        """递归检查函数调用"""
        if isinstance(call_node, ast.Call):
            if isinstance(call_node.func, ast.Name):
                func_name = call_node.func.id

                if func_name == "input":
                    input_info = {
                        "line": line_no,
                        "type": "interactive",
                        "context": context or "unknown",
                    }
                    self.input_calls.append(input_info)
                elif func_name == "eval":
                    self.eval_calls.append({"line": line_no, "context": context})
                elif func_name == "exec":
                    self.exec_calls.append({"line": line_no, "context": context})
                elif func_name == "print":
                    self.print_calls.append({"line": line_no, "context": context})

            # 检查是否是链式调用，如 input().split()
            elif isinstance(call_node.func, ast.Attribute):
                # 检查 Attribute.value
                if isinstance(call_node.func.value, ast.Name):
                    if call_node.func.value.id == "open":
                        pass
                    elif call_node.func.value.id == "random":
                        self.random_calls.append({"line": line_no, "method": call_node.func.attr})
                    # 检查是否是 input().split() 等链式调用
                    elif call_node.func.value.id == "input":
                        input_info = {
                            "line": line_no,
                            "type": "interactive",
                            "context": context or "unknown",
                            "is_chained": True,  # 标记为链式调用
                            "split_separator": None,  # 默认使用空格分隔
                        }
                        self.input_calls.append(input_info)
                        self.input_chained_calls.append(input_info)
                # 如果 Attribute.value 本身是一个 Call（如 input().split()），检查是否是 input().method() 模式
                elif isinstance(call_node.func.value, ast.Call):
                    # 检查这个 Call 是否是 input()
                    if isinstance(call_node.func.value.func, ast.Name) and call_node.func.value.func.id == "input":
                        # 提取 split() 的分隔符参数
                        split_separator = None
                        if call_node.func.attr == "split" and call_node.args:
                            if isinstance(call_node.args[0], ast.Constant):
                                split_separator = call_node.args[0].value
                        input_info = {
                            "line": line_no,
                            "type": "interactive",
                            "context": context or "unknown",
                            "is_chained": True,  # 标记为链式调用
                            "split_separator": split_separator,  # 存储分隔符
                        }
                        self.input_calls.append(input_info)
                        self.input_chained_calls.append(input_info)
                    # 递归检查这个 Call
                    self._check_call_function(call_node.func.value, line_no, context)

            # 递归检查 func 属性本身（处理 input().split() 等链式调用）
            if isinstance(call_node.func, ast.Call):
                self._check_call_function(call_node.func, line_no, context)

            # 递归检查参数中的函数调用
            for arg in call_node.args:
                if isinstance(arg, ast.Call):
                    self._check_call_function(arg, line_no, context)

            # 检查关键字参数
            for keyword in call_node.keywords:
                if isinstance(keyword.value, ast.Call):
                    self._check_call_function(keyword.value, line_no, context)

    def _check_subscript(self, node):
        """检查索引操作"""
        if isinstance(node, ast.Subscript):
            subscript_info = {
                "line": node.lineno if hasattr(node, 'lineno') else 0,
                "target": self._get_node_name(node.value),
            }
            self.subscript_ops.append(subscript_info)
            self.subscript_targets[node.value.id if isinstance(node.value, ast.Name) else None] = True

    def _check_division(self, node):
        """检查除法操作"""
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            self.division_ops.append({
                "line": node.lineno if hasattr(node, 'lineno') else 0,
                "op": type(node.op).__name__,
            })

    def _get_node_name(self, node):
        """获取节点名称"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return "unknown"

    # ==================== AST 访问方法 ====================

    def visit_FunctionDef(self, node):
        """访问函数定义"""
        # 检查是否是嵌套函数（通过检查父节点）
        is_nested = any(isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef))
                       for parent in self._get_ancestors(node))

        # 增加嵌套深度
        self.nested_depth += 1
        self.max_nested_depth = max(self.max_nested_depth, self.nested_depth)

        # 只记录顶层函数（非嵌套）
        if not is_nested:
            func_info = {
                "name": node.name,
                "line": node.lineno,
                "args": [arg.arg for arg in node.args.args],
                "has_return": any(isinstance(n, ast.Return) for n in ast.walk(node)),
                "arg_count": len(node.args.args),
            }
            self.functions.append(func_info)

        # 继续访问子节点
        self.generic_visit(node)

        # 减少嵌套深度
        self.nested_depth -= 1

    def _get_ancestors(self, node):
        """获取节点的祖先节点列表"""
        ancestors = []
        current = node
        while hasattr(current, '_parent') and current._parent:
            ancestors.append(current._parent)
            current = current._parent
        return ancestors

    def visit_Lambda(self, node):
        """访问 lambda 表达式"""
        self.lambda_count += 1
        self.generic_visit(node)

    def visit_Yield(self, node):
        """访问 yield 语句"""
        self.yield_count += 1
        self.generic_visit(node)

    def visit_YieldFrom(self, node):
        """访问 yield from 语句"""
        self.yield_count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """访问异步函数定义"""
        self.nested_depth += 1
        self.max_nested_depth = max(self.max_nested_depth, self.nested_depth)

        if self.nested_depth == 1:
            func_info = {
                "name": node.name,
                "line": node.lineno,
                "args": [arg.arg for arg in node.args.args],
                "has_return": True,
                "arg_count": len(node.args.args),
                "is_async": True,
            }
            self.functions.append(func_info)

        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_Call(self, node):
        """访问函数调用"""
        # 检查是否是 compile() 调用
        if isinstance(node.func, ast.Name) and node.func.id == "compile":
            self.compile_calls.append({"line": node.lineno})

        self.generic_visit(node)

    def visit_Assign(self, node):
        """访问赋值语句"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id not in self.global_vars:
                    self.global_vars.append(target.id)

        if isinstance(node.value, ast.Call):
            self._check_call_function(node.value, node.lineno, "assignment")
        elif isinstance(node.value, ast.BinOp):
            self._check_division(node.value)

        self.generic_visit(node)

    def visit_Expr(self, node):
        """访问表达式语句（顶层代码）"""
        if isinstance(node.value, ast.Call):
            self._check_call_function(node.value, node.lineno, "expression")
        elif isinstance(node.value, ast.BinOp):
            self._check_division(node.value)

        self.top_level_code.append({"type": "expr", "line": node.lineno})
        self.generic_visit(node)

    def visit_If(self, node):
        """访问 if 语句"""
        self.conditional_structures.append({
            "type": "if",
            "line": node.lineno,
        })

        if isinstance(node.test, ast.Compare):
            self.comparisons.append({
                "line": node.lineno,
                "type": "comparison",
            })

        self.nested_depth += 1
        self.max_nested_depth = max(self.max_nested_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_While(self, node):
        """访问 while 循环"""
        self.loop_structures.append({
            "type": "while",
            "line": node.lineno,
        })

        self.nested_depth += 1
        self.max_nested_depth = max(self.max_nested_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_For(self, node):
        """访问 for 循环"""
        self.loop_structures.append({
            "type": "for",
            "line": node.lineno,
        })

        self.nested_depth += 1
        self.max_nested_depth = max(self.max_nested_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_Try(self, node):
        """访问 try/except 块"""
        self.try_except_blocks.append({
            "line": node.lineno,
            "handler_count": len(node.handlers),
        })

        self.nested_depth += 1
        self.max_nested_depth = max(self.max_nested_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_Return(self, node):
        """访问 return 语句"""
        self.return_statements.append({"line": node.lineno if hasattr(node, 'lineno') else 0})
        self.generic_visit(node)

    def visit_Import(self, node):
        """访问 import 语句"""
        self.import_statements.append({"type": "import", "names": [alias.name for alias in node.names]})
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """访问 from ... import 语句"""
        self.import_statements.append({"type": "from_import", "module": node.module, "names": [alias.name for alias in node.names]})
        self.generic_visit(node)

    def visit_Subscript(self, node):
        """访问索引操作"""
        self._check_subscript(node)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """访问二元操作"""
        self._check_division(node)
        self.generic_visit(node)

    def visit_Compare(self, node):
        """访问比较操作"""
        self.comparisons.append({
            "line": node.lineno if hasattr(node, 'lineno') else 0,
            "type": "comparison",
        })
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """访问属性访问"""
        if isinstance(node.value, ast.Name):
            if node.value.id == "sys" and node.attr in ["stdin", "stdout", "stderr"]:
                if node.attr == "stdin":
                    self.stdin_sites.append({"line": node.lineno if hasattr(node, 'lineno') else 0})
                elif node.attr == "stdout":
                    self.stderr_sites.append({"line": node.lineno if hasattr(node, 'lineno') else 0})

        self.generic_visit(node)


class EnhancedWrapper:
    """增强型学生代码包装器"""

    def __init__(self):
        self.analyzer = EnhancedAnalyzer()
        self.wrapped_code = None
        self.analysis_result = None

    def wrap(self, code: str, auto_detect_inputs: bool = True,
             wrap_mode: str = "full") -> Tuple[str, Dict[str, Any]]:
        """包装学生代码"""
        self.analysis_result = self.analyzer.analyze(code)
        if not self.analysis_result["success"]:
            return code, self.analysis_result

        # 检查是否有顶层 input() 调用
        # 如果有，需要使用 _wrap_script_code 来正确处理
        inputs_info = self.analysis_result["inputs"]
        has_top_level_inputs = inputs_info["total_input_sites"] > 0

        # 如果有顶层 input() 调用，或者没有找到合适的入口函数，则使用脚本包装
        if has_top_level_inputs or not self.analysis_result["functions"]:
            self.wrapped_code = self._wrap_script_code(code, wrap_mode)
        else:
            self.wrapped_code = self._wrap_existing_functions(code, wrap_mode)

        return self.wrapped_code, self.analysis_result

    def _wrap_existing_functions(self, code: str, wrap_mode: str) -> str:
        """包装已有的函数"""
        lines = code.split('\n')
        wrapped_lines = []

        # 添加必要的导入语句
        wrapped_lines.append("from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_literal_eval, _se_int, _se_str, _se_float, _se_range")
        wrapped_lines.append("")

        wrapped_lines.append("")
        wrapped_lines.append("# === 增强型自动生成的包装函数 ===")

        entry_func = self._find_entry_function()
        inputs_info = self.analysis_result["inputs"]

        if entry_func:
            func_name = entry_func["name"]
            args = entry_func["args"]

            wrapped_lines.append(f"def _se_wrapper({', '.join(args)}):")

            if inputs_info["needs_input_model"]:
                wrapped_lines.extend(self._generate_input_handling(inputs_info))

            if self.analysis_result["outputs"]["return_count"] > 0:
                wrapped_lines.append(f"    return {func_name}({', '.join(args)})")
            else:
                wrapped_lines.append(f"    result = {func_name}({', '.join(args)})")
                wrapped_lines.append(f"    return result")

            wrapped_lines.append("")
        else:
            wrapped_lines.append("# 未找到合适的入口函数")
            wrapped_lines.append("def _se_wrapper():")
            wrapped_lines.append("    return None")
            wrapped_lines.append("")

        wrapped_lines.extend(self._generate_special_function_handlers(wrap_mode))

        wrapped_lines.append("# === 原代码开始 ===")
        for line in self._filter_main_block(code):
            wrapped_lines.append(line)
        wrapped_lines.append("# === 原代码结束 ===")

        return '\n'.join(wrapped_lines)

    def _wrap_script_code(self, code: str, wrap_mode: str) -> str:
        """包装脚本代码 - 方案A：保持学生代码为模块级，让 PyExZ3 的 AST 转换器处理"""
        lines = code.split('\n')

        wrapped_lines = []

        # 添加必要的导入语句（让 PyExZ3 的 AST 转换器能 hook input 等调用）
        wrapped_lines.append("from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range")
        wrapped_lines.append("")

        # 保留原代码中的 import 语句
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                wrapped_lines.append(line)

        wrapped_lines.append("")
        wrapped_lines.append("# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===")
        wrapped_lines.append("")

        # 保留学生代码为模块级（不包装在函数内）
        # 让 PyExZ3 的 AST 转换器在运行时 hook input() 等调用
        in_main_block = False
        main_block_indent = 0

        for line in lines:
            stripped = line.lstrip()

            if not stripped:
                wrapped_lines.append("")
                continue

            if stripped.startswith("import ") or stripped.startswith("from "):
                continue

            # 处理 if __name__ == '__main__' 块
            if "if __name__" in stripped and "__main__" in stripped:
                in_main_block = True
                main_block_indent = len(line) - len(stripped)
                wrapped_lines.append(line)
                continue

            if in_main_block:
                if stripped and not stripped.startswith('#'):
                    current_indent = len(line) - len(stripped)
                    if current_indent <= main_block_indent:
                        in_main_block = False
                wrapped_lines.append(line)
                continue

            # 其他代码直接保留（作为模块级代码）
            wrapped_lines.append(line)

        return '\n'.join(wrapped_lines)

    def _find_entry_function(self):
        """查找入口函数"""
        for func in self.analysis_result["functions"]:
            if func["name"] == "main" or func["name"] == "__main__":
                return func

        if self.analysis_result["functions"]:
            return max(self.analysis_result["functions"], key=lambda f: f["arg_count"])

        return None

    def _filter_main_block(self, code: str) -> List[str]:
        """过滤掉 if __name__ == '__main__' 块"""
        lines = code.split('\n')
        result = []
        in_main_block = False
        main_block_indent = 0

        for line in lines:
            stripped = line.lstrip()

            if "if __name__" in stripped and "__main__" in stripped:
                in_main_block = True
                main_block_indent = len(line) - len(stripped)
                continue

            if in_main_block:
                if stripped and not stripped.startswith('#'):
                    current_indent = len(line) - len(stripped)
                    if current_indent <= main_block_indent:
                        in_main_block = False
                    else:
                        continue

            result.append(line)

        return result

    def _generate_input_handling(self, inputs_info: Dict[str, Any]) -> List[str]:
        """生成输入处理代码"""
        lines = []
        total_inputs = inputs_info["total_input_sites"]

        if total_inputs > 0:
            args = [f"arg{i}" for i in range(total_inputs)]
            lines.append(f"    # 自动检测到 {total_inputs} 个输入点")
            lines.append(f"    # 参数: {', '.join(args)}")
            lines.append("")

            for i, input_info in enumerate(inputs_info["input_details"]):
                input_type = input_info.get("type", "interactive")
                is_chained = input_info.get("is_chained", False)

                if input_type == "interactive":
                    if is_chained:
                        lines.append(f"    arg{i} = _se_input('1 2 3')  # 链式调用需要非空输入")
                    else:
                        lines.append(f"    arg{i} = _se_input('请输入第{i+1}个值: ')")
                elif input_type == "file":
                    lines.append(f"    arg{i} = _se_read_file('input_{i}.txt')")
                elif input_type == "stdin":
                    if is_chained:
                        lines.append(f"    arg{i} = _se_input('1 2 3')  # 链式调用需要非空输入")
                    else:
                        lines.append(f"    arg{i} = _se_input('')")
                else:
                    if is_chained:
                        lines.append(f"    arg{i} = '1 2 3'  # 链式调用需要非空输入")
                    else:
                        lines.append(f"    arg{i} = None")

            lines.append("")
        else:
            lines.append("    pass")

        return lines

    def _generate_special_function_handlers(self, wrap_mode: str) -> List[str]:
        """生成特殊函数处理代码"""
        lines = []
        special_info = self.analysis_result["special_functions"]

        if wrap_mode == "minimal":
            return lines

        lines.append("    # === 特殊函数安全包装 ===")

        if special_info["eval_count"] > 0:
            lines.append("    def _se_safe_eval(expr):")
            lines.append("        return eval(expr)")
            lines.append("")

        if special_info["exec_count"] > 0:
            lines.append("    def _se_safe_exec(code):")
            lines.append("        return None")
            lines.append("")

        if special_info["open_count"] > 0:
            lines.append("    def _se_safe_open(filename, mode='r'):")
            lines.append("        # 文件操作在符号执行中无法处理，返回 None")
            lines.append("        # 如需测试文件相关代码，请提供模拟数据")
            lines.append("        return None")
            lines.append("")

        if special_info["random_count"] > 0:
            lines.append("    def _se_safe_random():")
            lines.append("        return 0")
            lines.append("")

        if special_info["time_count"] > 0:
            lines.append("    def _se_safe_time():")
            lines.append("        return 0")
            lines.append("")

        return lines

    def _process_output_statement(self, line: str, outputs_info: Dict[str, Any]) -> Tuple[str, bool]:
        """处理输出语句"""
        stripped = line.lstrip()

        # 检查是否包含 print(
        if 'print(' not in stripped:
            return stripped, False

        # 找到 print( 的位置
        print_pos = stripped.index('print(')

        # 检查是否有赋值语句（x = print(...) 形式）
        # 我们需要忽略 print 的返回值，只保留其副作用
        if '=' in stripped[:print_pos]:
            assign_part = stripped[:print_pos].strip()
            # 排除 if、elif 等关键字
            keywords = {'if', 'elif', 'while', 'for', 'and', 'or', 'not', 'in', 'is'}
            if assign_part and assign_part not in keywords:
                # 这是 x = print(...) 形式，我们忽略它
                return stripped, False

        # 找到对应的右括号
        start = print_pos + 6  # "print(" 的长度
        paren_count = 1
        end = start
        for j in range(start, len(stripped)):
            if stripped[j] == '(':
                paren_count += 1
            elif stripped[j] == ')':
                paren_count -= 1
                if paren_count == 0:
                    end = j
                    break

        # 提取 print 内容
        print_content = stripped[start:end]

        # 处理多参数情况：print(a, b, c) -> result = (a, b, c)
        if ',' in print_content:
            print_content = f"({print_content})"

        # 构建结果语句
        indent = len(line) - len(stripped)
        return ' ' * indent + f"result = {print_content}", False


def wrap_student_code(input_file: str, output_file: Optional[str] = None,
                      auto_detect_inputs: bool = True,
                      wrap_mode: str = "full",
                      show_analysis: bool = True) -> bool:
    """包装学生代码文件"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()

        wrapper = EnhancedWrapper()
        wrapped_code, analysis_result = wrapper.wrap(code, auto_detect_inputs, wrap_mode)

        if not analysis_result["success"]:
            print(f"错误: {analysis_result['error']}")
            return False

        if show_analysis:
            print("=" * 70)
            print("增强型学生代码分析结果")
            print("=" * 70)

            print(f"\n【基本信息】")
            print(f"  函数定义: {len(analysis_result['functions'])} 个")
            for func in analysis_result['functions']:
                args_str = ', '.join(func['args']) if func['args'] else '(无参数)'
                print(f"    - {func['name']}({args_str}) @ 行 {func['line']}")

            inputs = analysis_result['inputs']
            print(f"\n【输入分析】")
            print(f"  交互式输入: {inputs['interactive_count']} 处")
            print(f"  文件输入: {inputs['file_input_count']} 处")
            print(f"  stdin 输入: {inputs['stdin_count']} 处")
            print(f"  随机数输入: {inputs['random_count']} 处")

            outputs = analysis_result['outputs']
            print(f"\n【输出分析】")
            print(f"  print() 输出: {outputs['print_count']} 处")
            print(f"  返回值: {'有' if outputs['return_count'] > 0 else '无'}")

            special = analysis_result['special_functions']
            print(f"\n【特殊函数】")
            print(f"  eval() 调用: {special['eval_count']} 处")
            print(f"  exec() 调用: {special['exec_count']} 处")

            cf = analysis_result['control_flow']
            print(f"\n【控制流】")
            print(f"  循环结构: {cf['loop_count']} 个")
            print(f"  最大嵌套深度: {cf['max_nested_depth']}")

            bc = analysis_result['boundary_conditions']
            print(f"\n【边界条件】")
            print(f"  除法操作: {bc['division_count']} 处")
            print(f"  索引操作: {bc['subscript_count']} 处")

            print(f"\n【代码复杂度评分】: {analysis_result['complexity_score']}")

            if analysis_result['warnings']:
                print(f"\n【警告信息】")
                for warning in analysis_result['warnings']:
                    print(f"  [WARNING] {warning}")

            print("=" * 70)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(wrapped_code)
            print(f"\n包装后的代码已保存到: {output_file}")
        else:
            base, ext = os.path.splitext(input_file)
            output_file = f"{base}_enhanced_wrapped{ext}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(wrapped_code)
            print(f"\n包装后的代码已保存到: {output_file}")

        if show_analysis:
            print("\n" + "=" * 70)
            print("包装后的代码预览 (前1000字符)")
            print("=" * 70)
            print(wrapped_code[:1000])
            if len(wrapped_code) > 1000:
                print(f"... (共 {len(wrapped_code)} 字符)")
            print("=" * 70)

        return True

    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="增强型学生代码自动包装器 V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('input_file', nargs='?', help='输入的学生代码文件')
    parser.add_argument('-o', '--output', dest='output_file', help='输出文件路径')
    parser.add_argument('-m', '--mode', dest='wrap_mode', choices=['full', 'minimal', 'safe'], default='full')
    parser.add_argument('-a', '--auto-detect', dest='auto_detect', type=bool, default=True)
    parser.add_argument('--no-analysis', dest='show_analysis', action='store_false', default=True)
    parser.add_argument('-c', '--code', dest='code', type=str, default=None)

    args = parser.parse_args()

    if not args.input_file and not args.code:
        parser.print_help()
        return 0

    if args.code:
        wrapper = EnhancedWrapper()
        wrapped_code, analysis_result = wrapper.wrap(args.code, args.auto_detect, args.wrap_mode)

        if not analysis_result["success"]:
            print(f"错误: {analysis_result['error']}")
            return 1

        if args.show_analysis:
            print("=" * 70)
            print("增强型学生代码分析结果")
            print("=" * 70)
            print(f"  函数定义: {len(analysis_result['functions'])} 个")
            print(f"  输入点: {analysis_result['inputs']['total_input_sites']} 个")
            print(f"  复杂度评分: {analysis_result['complexity_score']}")
            print("=" * 70)
            print("\n包装后的代码:")
            print("=" * 70)

        print(wrapped_code)
        return 0

    success = wrap_student_code(
        args.input_file,
        args.output_file,
        args.auto_detect,
        args.wrap_mode,
        args.show_analysis
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
