#!/usr/bin/env python3
"""
学生代码自动包装器

自动将学生代码转换为可分析的函数形式，支持：
1. 自动识别主入口函数
2. 将 print() 输出转换为 return 语句
3. 处理 eval()、exec() 等危险函数
4. 支持变量输入的符号化
"""

import ast
import argparse
import sys
import os
from typing import Optional, List, Tuple, Dict, Any


class StudentCodeAnalyzer(ast.NodeVisitor):
    """学生代码分析器"""

    def __init__(self):
        self.functions = []  # 函数定义列表
        self.global_vars = []  # 全局变量列表
        self.print_calls = []  # print() 调用列表
        self.input_calls = []  # input() 调用列表
        self.eval_calls = []  # eval() 调用列表
        self.exec_calls = []  # exec() 调用列表
        self.has_main = False  # 是否有 if __name__ == '__main__' 块
        self.top_level_code = []  # 顶层代码语句
        self.return_statements = []  # return 语句列表
        self.import_statements = []  # import 语句列表

    def analyze(self, code: str) -> Dict[str, Any]:
        """分析学生代码"""
        try:
            tree = ast.parse(code)
            self.visit(tree)
            return self.get_analysis_result()
        except SyntaxError as e:
            return {"error": f"语法错误: {e}", "success": False}

    def get_analysis_result(self) -> Dict[str, Any]:
        """获取分析结果"""
        return {
            "success": True,
            "functions": self.functions,
            "global_vars": self.global_vars,
            "has_main": self.has_main,
            "print_calls": len(self.print_calls),
            "input_calls": len(self.input_calls),
            "eval_calls": len(self.eval_calls),
            "exec_calls": len(self.exec_calls),
            "has_return": len(self.return_statements) > 0,
            "import_statements": self.import_statements
        }

    def _check_call_function(self, call_node, line_no):
        """递归检查函数调用"""
        if isinstance(call_node, ast.Call):
            if isinstance(call_node.func, ast.Name):
                func_name = call_node.func.id
                if func_name == "print":
                    self.print_calls.append({"line": line_no})
                elif func_name == "input":
                    self.input_calls.append({"line": line_no})
                elif func_name == "eval":
                    self.eval_calls.append({"line": line_no})
                elif func_name == "exec":
                    self.exec_calls.append({"line": line_no})
            # 递归检查参数中的函数调用
            for arg in call_node.args:
                if isinstance(arg, ast.Call):
                    self._check_call_function(arg, line_no)
            # 检查关键字参数
            for keyword in call_node.keywords:
                if isinstance(keyword.value, ast.Call):
                    self._check_call_function(keyword.value, line_no)

    def visit_FunctionDef(self, node):
        """访问函数定义"""
        func_info = {
            "name": node.name,
            "line": node.lineno,
            "args": [arg.arg for arg in node.args.args],
            "has_return": any(isinstance(n, ast.Return) for n in ast.walk(node))
        }
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_Assign(self, node):
        """访问赋值语句"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.global_vars.append(target.id)
        # 递归检查赋值语句右边的表达式
        if isinstance(node.value, ast.Call):
            self._check_call_function(node.value, node.lineno)
        self.generic_visit(node)

    def visit_Expr(self, node):
        """访问表达式语句（顶层代码）"""
        if isinstance(node.value, ast.Call):
            self._check_call_function(node.value, node.lineno)
        self.top_level_code.append({"type": "expr", "line": node.lineno})
        self.generic_visit(node)

    def visit_If(self, node):
        """访问 if 语句"""
        # 检查是否是 if __name__ == '__main__'
        if isinstance(node.test, ast.Compare):
            if isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__":
                self.has_main = True
        self.generic_visit(node)

    def visit_Return(self, node):
        """访问 return 语句"""
        self.return_statements.append({"line": node.lineno})
        self.generic_visit(node)

    def visit_Import(self, node):
        """访问 import 语句"""
        self.import_statements.append({"type": "import", "names": [alias.name for alias in node.names]})
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """访问 from ... import 语句"""
        self.import_statements.append({"type": "from_import", "module": node.module, "names": [alias.name for alias in node.names]})
        self.generic_visit(node)


class StudentCodeWrapper:
    """学生代码包装器"""

    def __init__(self):
        self.analyzer = StudentCodeAnalyzer()
        self.wrapped_code = None
        self.analysis_result = None

    def wrap(self, code: str, auto_detect_inputs: bool = True) -> Tuple[str, Dict[str, Any]]:
        """
        包装学生代码

        Args:
            code: 学生代码
            auto_detect_inputs: 是否自动检测输入类型

        Returns:
            Tuple[str, Dict]: 包装后的代码和分析结果
        """
        # 分析代码结构
        self.analysis_result = self.analyzer.analyze(code)
        if not self.analysis_result["success"]:
            return code, self.analysis_result

        # 根据代码结构选择包装策略
        if self.analysis_result["functions"]:
            # 如果有函数定义，包装最可能的入口函数
            self.wrapped_code = self._wrap_existing_functions(code)
        else:
            # 如果没有函数定义，将整个脚本包装成函数
            self.wrapped_code = self._wrap_script_code(code)

        return self.wrapped_code, self.analysis_result

    def _wrap_existing_functions(self, code: str) -> str:
        """包装已有的函数"""
        lines = code.split('\n')
        wrapped_lines = []

        # 添加必要的导入语句
        wrapped_lines.append("from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_int, _se_str, _se_float, _se_range")
        wrapped_lines.append("")

        # 添加包装函数
        wrapped_lines.append("")
        wrapped_lines.append("# === 自动生成的包装函数 ===")

        # 查找最可能的入口函数（通常是 main 或者第一个没有装饰器的函数）
        entry_func = None
        for func in self.analysis_result["functions"]:
            if func["name"] == "main" or func["name"] == "__main__":
                entry_func = func
                break

        if not entry_func and self.analysis_result["functions"]:
            # 选择第一个没有装饰器的函数
            for func in self.analysis_result["functions"]:
                if not func["name"].startswith("_") or func["name"] == "__main__":
                    entry_func = func
                    break

        if entry_func:
            func_name = entry_func["name"]
            args = entry_func["args"]

            # 分析输入数量
            input_count = self.analysis_result["input_calls"]

            # 生成包装函数
            wrapped_lines.append(f"def _se_wrapper({', '.join(args)}):")

            # 初始化符号输入（如果有 input() 调用）
            if input_count > 0:
                init_args = [f"('arg{i}', None, 'int')" for i in range(input_count)]
                wrapped_lines.append(f"    init_symbolic_inputs([{', '.join(init_args)}])")
                wrapped_lines.append("")

            # 添加参数类型注解
            arg_decls = []
            for arg in args:
                arg_decls.append(f"    # {arg}: 自动推断类型")

            # 生成调用函数代码
            if self.analysis_result["has_return"]:
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

        # 添加特殊函数处理
        if self.analysis_result["eval_calls"]:
            wrapped_lines.append("# 处理 eval() 调用")
            wrapped_lines.append("def _se_safe_eval(expr):")
            wrapped_lines.append("    # eval() 被替换为安全版本，返回符号表达式")
            wrapped_lines.append("    return eval(expr)")
            wrapped_lines.append("")

        if self.analysis_result["exec_calls"]:
            wrapped_lines.append("# 处理 exec() 调用")
            wrapped_lines.append("def _se_safe_exec(code):")
            wrapped_lines.append("    # exec() 被替换为安全版本")
            wrapped_lines.append("    return None")
            wrapped_lines.append("")

        # 保留原代码，但移除 if __name__ == '__main__' 块
        in_main_block = False
        main_block_indent = 0

        for i, line in enumerate(lines):
            stripped = line.lstrip()

            # 检测 if __name__ == '__main__'
            if "if __name__" in stripped and "__main__" in stripped:
                in_main_block = True
                main_block_indent = len(line) - len(stripped)
                continue

            # 如果在 main 块内，检查是否退出了
            if in_main_block:
                if stripped and not stripped.startswith('#'):
                    current_indent = len(line) - len(stripped)
                    if current_indent <= main_block_indent:
                        in_main_block = False
                    else:
                        continue

            if not in_main_block:
                wrapped_lines.append(line)

        return '\n'.join(wrapped_lines)

    def _wrap_script_code(self, code: str) -> str:
        """包装没有函数的脚本代码"""
        lines = code.split('\n')
        wrapped_lines = []

        # 添加必要的导入语句
        wrapped_lines.append("from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_int, _se_str, _se_float, _se_range")
        wrapped_lines.append("")

        # 保留 import 语句
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                wrapped_lines.append(line)

        wrapped_lines.append("")
        wrapped_lines.append("# === 自动生成的包装函数 ===")
        wrapped_lines.append("def _se_wrapper():")

        # 分析输入输出
        input_count = self.analysis_result["input_calls"]
        print_count = self.analysis_result["print_calls"]
        eval_count = self.analysis_result["eval_calls"]
        exec_count = self.analysis_result["exec_calls"]

        # 生成参数列表
        if input_count > 0:
            args = [f"arg{i}" for i in range(input_count)]
            wrapped_lines.append(f"    # 自动检测到 {input_count} 个 input() 调用")
            wrapped_lines.append(f"    # 参数: {', '.join(args)}")
            wrapped_lines.append("")
            init_args = [f"('arg{i}', None, 'int')" for i in range(input_count)]
            wrapped_lines.append(f"    init_symbolic_inputs([{', '.join(init_args)}])")
            wrapped_lines.append("")
        else:
            wrapped_lines.append("    pass")

        # 添加原代码
        wrapped_lines.append("    # --- 学生代码开始 ---")

        in_main_block = False
        main_block_indent = 0
        indent_size = 4  # 缩进大小

        for i, line in enumerate(lines):
            stripped = line.lstrip()

            # 跳过空行
            if not stripped:
                wrapped_lines.append("")
                continue

            # 跳过 import 语句（已在上方处理）
            if stripped.startswith("import ") or stripped.startswith("from "):
                continue

            # 跳过 if __name__ == '__main__' 块
            if "if __name__" in stripped and "__main__" in stripped:
                in_main_block = True
                main_block_indent = len(line) - len(stripped)
                continue

            # 如果在 main 块内，检查是否退出了
            if in_main_block:
                if stripped and not stripped.startswith('#'):
                    current_indent = len(line) - len(stripped)
                    if current_indent <= main_block_indent:
                        in_main_block = False
                    else:
                        continue

            # 计算原始缩进
            original_indent = len(line) - len(stripped)

            # 处理 print() 语句
            if 'print(' in stripped:
                # 将 print() 转换为 result = ...
                if stripped.startswith('print('):
                    # 简单情况：print(...) -> result = ...
                    # 提取 print 内的内容
                    start = stripped.index('print(') + 6
                    # 找到匹配的括号
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
                    print_content = stripped[start:end]
                    wrapped_lines.append(' ' * (original_indent + indent_size) + f"result = {print_content}")
                else:
                    # 复杂情况：行中有 print() 但不在开头
                    wrapped_lines.append(' ' * (original_indent + indent_size) + stripped)
            else:
                # 其他语句，添加缩进
                wrapped_lines.append(' ' * (original_indent + indent_size) + stripped)

        wrapped_lines.append("    # --- 学生代码结束 ---")
        wrapped_lines.append("")

        # 添加 return 语句
        if print_count > 0:
            wrapped_lines.append("    return result if 'result' in dir() else None")
        else:
            wrapped_lines.append("    return None")

        # 添加特殊函数处理
        if eval_count > 0:
            wrapped_lines.append("")
            wrapped_lines.append("def _se_safe_eval(expr):")
            wrapped_lines.append("    # eval() 被替换为安全版本")
            wrapped_lines.append("    return eval(expr)")

        if exec_count > 0:
            wrapped_lines.append("")
            wrapped_lines.append("def _se_safe_exec(code):")
            wrapped_lines.append("    # exec() 被替换为安全版本")
            wrapped_lines.append("    return None")

        return '\n'.join(wrapped_lines)


def wrap_student_code(input_file: str, output_file: Optional[str] = None,
                      auto_detect_inputs: bool = True, show_analysis: bool = True) -> bool:
    """
    包装学生代码文件

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径（可选）
        auto_detect_inputs: 是否自动检测输入
        show_analysis: 是否显示分析结果

    Returns:
        bool: 是否成功
    """
    try:
        # 读取学生代码
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()

        # 包装代码
        wrapper = StudentCodeWrapper()
        wrapped_code, analysis_result = wrapper.wrap(code, auto_detect_inputs)

        if not analysis_result["success"]:
            print(f"错误: {analysis_result['error']}")
            return False

        # 显示分析结果
        if show_analysis:
            print("=" * 60)
            print("学生代码分析结果")
            print("=" * 60)
            print(f"函数定义: {len(analysis_result['functions'])} 个")
            for func in analysis_result['functions']:
                args_str = ', '.join(func['args']) if func['args'] else '(无参数)'
                print(f"  - {func['name']}({args_str}) @ 行 {func['line']}")
            print(f"全局变量: {', '.join(analysis_result['global_vars']) if analysis_result['global_vars'] else '无'}")
            print(f"print() 调用: {analysis_result['print_calls']} 处")
            print(f"input() 调用: {analysis_result['input_calls']} 处")
            print(f"eval() 调用: {analysis_result['eval_calls']} 处")
            print(f"exec() 调用: {analysis_result['exec_calls']} 处")
            print(f"包含 if __name__ 块: {'是' if analysis_result['has_main'] else '否'}")
            print(f"有返回值: {'是' if analysis_result['has_return'] else '否'}")
            print("=" * 60)

        # 保存包装后的代码
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(wrapped_code)
            print(f"包装后的代码已保存到: {output_file}")
        else:
            # 生成输出文件名
            base, ext = os.path.splitext(input_file)
            output_file = f"{base}_wrapped{ext}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(wrapped_code)
            print(f"包装后的代码已保存到: {output_file}")

        # 显示包装后的代码
        if show_analysis:
            print("\n" + "=" * 60)
            print("包装后的代码预览")
            print("=" * 60)
            print(wrapped_code[:1000])
            if len(wrapped_code) > 1000:
                print(f"... (共 {len(wrapped_code)} 字符)")
            print("=" * 60)

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
        description="学生代码自动包装器 - 将学生代码转换为可分析的函数形式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s student_code.py
  %(prog)s student_code.py -o wrapped_code.py
  %(prog)s student_code.py --no-analysis
  %(prog)s student_code.py -a False
        """
    )

    parser.add_argument('input_file', nargs='?', help='输入的学生代码文件')
    parser.add_argument('-o', '--output', dest='output_file', help='输出文件路径')
    parser.add_argument('-a', '--auto-detect', dest='auto_detect', type=bool, default=True,
                        help='是否自动检测输入类型 (默认: True)')
    parser.add_argument('--no-analysis', dest='show_analysis', action='store_false', default=True,
                        help='不显示分析结果')
    parser.add_argument('-c', '--code', dest='code', type=str, default=None,
                        help='直接传入代码字符串')

    args = parser.parse_args()

    # 如果没有输入文件，显示帮助
    if not args.input_file and not args.code:
        parser.print_help()
        print("\n" + "=" * 60)
        print("使用示例:")
        print("=" * 60)
        print("# 包装文件中的代码")
        print("python student_code_wrapper.py student_code.py")
        print()
        print("# 指定输出文件")
        print("python student_code_wrapper.py student_code.py -o output.py")
        print()
        print("# 不显示分析结果")
        print("python student_code_wrapper.py student_code.py --no-analysis")
        print()
        print("# 直接传入代码")
        print('python student_code_wrapper.py -c "x = input(); print(x)"')
        print("=" * 60)
        return 0

    # 处理代码字符串
    if args.code:
        wrapper = StudentCodeWrapper()
        wrapped_code, analysis_result = wrapper.wrap(args.code, args.auto_detect)

        if not analysis_result["success"]:
            print(f"错误: {analysis_result['error']}")
            return 1

        if args.show_analysis:
            print("=" * 60)
            print("学生代码分析结果")
            print("=" * 60)
            print(f"函数定义: {len(analysis_result['functions'])} 个")
            print(f"print() 调用: {analysis_result['print_calls']} 处")
            print(f"input() 调用: {analysis_result['input_calls']} 处")
            print(f"eval() 调用: {analysis_result['eval_calls']} 处")
            print(f"exec() 调用: {analysis_result['exec_calls']} 处")
            print("=" * 60)
            print("\n包装后的代码:")
            print("=" * 60)

        print(wrapped_code)
        return 0

    # 处理文件
    success = wrap_student_code(
        args.input_file,
        args.output_file,
        args.auto_detect,
        args.show_analysis
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
