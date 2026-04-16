import os
import time
import json
from hashlib import sha256

class SMTExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _convert_expr_to_smt(self, expr):
        """Convert PyExZ3 expression to SMT format"""
        if isinstance(expr, list):
            op = expr[0]
            args = expr[1:]
            
            if op == "=":
                return f"(= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "not":
                return f"(not {self._convert_expr_to_smt(args[0])})"
            elif op == "<":
                return f"(< {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == ">":
                return f"(> {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "<=":
                return f"(<= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == ">=":
                return f"(>= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "+":
                return f"(+ {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "-":
                if len(args) == 1:
                    return f"(- {self._convert_expr_to_smt(args[0])})"
                else:
                    return f"(- {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "*":
                return f"(* {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "/":
                return f"(/ {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "%":
                return f"(mod {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "abs":
                return f"(abs {self._convert_expr_to_smt(args[0])})"
            elif op == "and":
                return f"(and {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "or":
                return f"(or {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "xor":
                return f"(xor {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "str.<":
                return f"(str.< {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "str.<=":
                return f"(str.<= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            else:
                return f"; Unsupported operator: {op}"
        elif isinstance(expr, str):
            return f'"{expr}"'
        elif isinstance(expr, (int, float)):
            return str(expr)
        else:
            # Handle symbolic variables
            if hasattr(expr, 'name'):
                # 确保返回符号变量名，而不是具体值
                return expr.name
            # 处理其他情况
            return str(expr)
    
    def _convert_predicate_to_smt(self, predicate):
        """Convert predicate to SMT format"""
        sym_type = predicate.symtype
        result = predicate.result
        
        # 确保使用符号表达式，而不是具体值
        if hasattr(sym_type, 'expr') and sym_type.expr:
            # 处理表达式中的具体值问题
            # 从predicate.get_symbolic_expr()获取纯符号表达式
            symbolic_expr_str = predicate.get_symbolic_expr()
            # 解析并转换为SMT格式
            smt_expr = self._parse_symbolic_expr(symbolic_expr_str)
        else:
            # 对于变量情况，使用变量名
            if hasattr(sym_type, 'name'):
                smt_expr = sym_type.name
            else:
                smt_expr = str(sym_type)
        
        if not result:
            smt_expr = f"(not {smt_expr})"
        
        return smt_expr
    
    def _parse_symbolic_expr(self, expr_str):
        """解析符号表达式字符串并转换为SMT格式"""
        # 移除括号
        expr_str = expr_str.strip()
        if expr_str.startswith('(') and expr_str.endswith(')'):
            expr_str = expr_str[1:-1].strip()
        
        # 分割表达式
        parts = []
        current_part = ''
        depth = 0
        
        for char in expr_str:
            if char == '(':
                depth += 1
                current_part += char
            elif char == ')':
                depth -= 1
                current_part += char
            elif char == ' ' and depth == 0:
                if current_part:
                    parts.append(current_part)
                    current_part = ''
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        if not parts:
            return expr_str
        
        op = parts[0]
        args = parts[1:]
        
        # 处理不同的操作符
        if op == '<':
            return f"(< {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '>':
            return f"(> {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '<=':
            return f"(<= {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '>=':
            return f"(>= {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '==':
            return f"(= {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '!=':
            return f"(not (= {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])}))"
        elif op == '+':
            return f"(+ {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '-':
            if len(args) == 1:
                return f"(- {self._parse_symbolic_expr(args[0])})"
            else:
                return f"(- {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '*':
            return f"(* {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == '/':
            return f"(/ {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == 'mod':
            return f"(mod {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == 'abs':
            return f"(abs {self._parse_symbolic_expr(args[0])})"
        elif op == 'and':
            return f"(and {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == 'or':
            return f"(or {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        elif op == 'xor':
            return f"(xor {self._parse_symbolic_expr(args[0])} {self._parse_symbolic_expr(args[1])})"
        else:
            # 处理变量或常量
            return op
    
    def _extract_variables(self, asserts, query):
        """提取所有变量并按字母顺序排序"""
        variables = set()
        
        def extract_vars(expr):
            if isinstance(expr, list):
                for arg in expr[1:]:
                    extract_vars(arg)
            elif hasattr(expr, 'name'):
                variables.add(expr.name)
            elif hasattr(expr, 'expr') and expr.expr:
                extract_vars(expr.expr)
            elif hasattr(expr, 'get_symbolic_expr'):
                # 从符号表达式字符串中提取变量
                expr_str = expr.get_symbolic_expr()
                # 简单的变量提取逻辑，提取所有可能的变量名
                import re
                # 匹配变量名（字母开头，后跟字母、数字或下划线）
                var_matches = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expr_str)
                # 过滤掉操作符和关键字
                operators = {'<', '>', '<=', '>=', '==', '!=', '+', '-', '*', '/', 'mod', 'abs', 'and', 'or', 'xor'}
                for var in var_matches:
                    if var not in operators:
                        variables.add(var)
        
        # 从断言中提取变量
        for assert_pred in asserts:
            if hasattr(assert_pred, 'symtype'):
                extract_vars(assert_pred.symtype)
            # 同时从符号表达式字符串中提取变量，确保不遗漏
            if hasattr(assert_pred, 'get_symbolic_expr'):
                extract_vars(assert_pred)
        
        # 从查询中提取变量
        if hasattr(query, 'symtype'):
            extract_vars(query.symtype)
        # 同时从符号表达式字符串中提取变量，确保不遗漏
        if hasattr(query, 'get_symbolic_expr'):
            extract_vars(query)
        
        # 按字母顺序排序，确保一致性
        return sorted(variables)
    
    def _generate_path_id(self, asserts, query):
        """生成路径的唯一标识符"""
        # 收集所有断言和查询的符号表达式
        expressions = []
        for assert_pred in asserts:
            if hasattr(assert_pred, 'get_symbolic_expr'):
                expr = assert_pred.get_symbolic_expr()
                expressions.append(f"{expr}:{assert_pred.result}")
        
        if query and hasattr(query, 'get_symbolic_expr'):
            expr = query.get_symbolic_expr()
            expressions.append(f"query:{expr}:{query.result}")
        
        # 按顺序排序，确保一致性
        expressions.sort()
        
        # 生成哈希值作为路径ID
        hash_input = ''.join(expressions)
        path_id = sha256(hash_input.encode()).hexdigest()[:16]
        
        return path_id
    
    def export_path(self, solver, asserts, query):
        """Export path constraints to SMT2 format"""
        # 生成路径ID
        path_id = self._generate_path_id(asserts, query)
        
        smt_content = "(set-logic ALL)\n"
        
        # 添加元信息
        # 确保solver是字符串类型
        if hasattr(solver, 'name'):
            solver_name = solver.name
        elif hasattr(solver, '__class__'):
            solver_name = solver.__class__.__name__
        else:
            solver_name = str(solver) if solver else "unknown"
        
        smt_content += f"; Path ID: {path_id}\n"
        smt_content += f"; Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        smt_content += f"; Solver: {solver_name}\n"
        smt_content += f"; Number of assertions: {len(asserts)}\n"
        smt_content += f"; Has query: {bool(query)}\n"
        smt_content += "\n"
        
        # 提取并排序变量
        variables = self._extract_variables(asserts, query)
        
        # 声明变量（默认使用Int类型）
        for var in variables:
            smt_content += f"(declare-const {var} Int)\n"
        smt_content += "\n"
        
        # 添加断言
        for assert_pred in asserts:
            smt_expr = self._convert_predicate_to_smt(assert_pred)
            # 使用get_symbolic_expr()方法获取纯符号表达式作为注释
            symbolic_expr = assert_pred.get_symbolic_expr() if hasattr(assert_pred, 'get_symbolic_expr') else str(assert_pred)
            smt_content += f"; ({symbolic_expr}) ({assert_pred.result})\n"
            smt_content += f"(assert {smt_expr})\n"
        smt_content += "\n"
        
        # 添加查询
        if query:
            query_expr = self._convert_predicate_to_smt(query)
            # 使用get_symbolic_expr()方法获取纯符号表达式作为注释
            symbolic_expr = query.get_symbolic_expr() if hasattr(query, 'get_symbolic_expr') else str(query)
            smt_content += f"; Query: ({symbolic_expr}) ({query.result})\n"
            smt_content += f"(assert (not {query_expr}))\n"
            smt_content += "\n"
        
        # 添加检查和模型获取
        smt_content += "(check-sat)\n"
        smt_content += "(get-model)\n"
        
        # 写入文件
        smt_file = os.path.join(self.output_dir, f"path_{path_id}.smt2")
        with open(smt_file, "w") as f:
            f.write(smt_content)
        
        # 同时生成路径信息JSON文件，便于后续分析
        # 确保solver是字符串类型
        if hasattr(solver, 'name'):
            solver_name = solver.name
        elif hasattr(solver, '__class__'):
            solver_name = solver.__class__.__name__
        else:
            solver_name = str(solver) if solver else "unknown"
        
        path_info = {
            "path_id": path_id,
            "timestamp": time.time(),
            "solver": solver_name,
            "assertions_count": len(asserts),
            "has_query": bool(query),
            "variables": variables,
            "smt_file": os.path.basename(smt_file)
        }
        
        with open(os.path.join(self.output_dir, f"path_{path_id}.json"), "w") as f:
            json.dump(path_info, f, indent=2)
        
        # 保留原有的path.smt2作为最新路径
        with open(os.path.join(self.output_dir, "path.smt2"), "w") as f:
            f.write(smt_content)
    
    def export_frontier(self, solver, frontier):
        """Export frontier constraints to SMT2 format"""
        frontier_dir = os.path.join(self.output_dir, "frontier")
        os.makedirs(frontier_dir, exist_ok=True)
        
        frontier_summary = []
        
        for i, constraint in enumerate(frontier):
            asserts, query = constraint.getAssertsAndQuery()
            
            # 生成约束ID
            path_id = self._generate_path_id(asserts, query)
            
            smt_content = "(set-logic ALL)\n"
            
            # 添加元信息
            # 确保solver是字符串类型
            if hasattr(solver, 'name'):
                solver_name = solver.name
            elif hasattr(solver, '__class__'):
                solver_name = solver.__class__.__name__
            else:
                solver_name = str(solver) if solver else "unknown"
            
            smt_content += f"; Constraint ID: {path_id}\n"
            smt_content += f"; Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            smt_content += f"; Solver: {solver_name}\n"
            smt_content += f"; Number of assertions: {len(asserts)}\n"
            smt_content += f"; Has query: {bool(query)}\n"
            smt_content += "\n"
            
            # 提取并排序变量
            variables = self._extract_variables(asserts, query)
            
            # 声明变量（默认使用Int类型）
            for var in variables:
                smt_content += f"(declare-const {var} Int)\n"
            smt_content += "\n"
            
            # 添加断言
            for assert_pred in asserts:
                smt_expr = self._convert_predicate_to_smt(assert_pred)
                # 使用get_symbolic_expr()方法获取纯符号表达式作为注释
                symbolic_expr = assert_pred.get_symbolic_expr() if hasattr(assert_pred, 'get_symbolic_expr') else str(assert_pred)
                smt_content += f"; ({symbolic_expr}) ({assert_pred.result})\n"
                smt_content += f"(assert {smt_expr})\n"
            smt_content += "\n"
            
            # 添加查询
            if query:
                query_expr = self._convert_predicate_to_smt(query)
                # 使用get_symbolic_expr()方法获取纯符号表达式作为注释
                symbolic_expr = query.get_symbolic_expr() if hasattr(query, 'get_symbolic_expr') else str(query)
                smt_content += f"; Query: ({symbolic_expr}) ({query.result})\n"
                smt_content += f"(assert (not {query_expr}))\n"
                smt_content += "\n"
            
            # 添加检查和模型获取
            smt_content += "(check-sat)\n"
            smt_content += "(get-model)\n"
            
            # 写入文件
            smt_file = os.path.join(frontier_dir, f"frontier_{i}_{path_id}.smt2")
            with open(smt_file, "w") as f:
                f.write(smt_content)
            
            # 添加到摘要
            frontier_summary.append({
                "constraint_id": path_id,
                "index": i,
                "assertions_count": len(asserts),
                "has_query": bool(query),
                "variables_count": len(variables),
                "smt_file": os.path.basename(smt_file)
            })
        
        # 写入摘要文件
        with open(os.path.join(frontier_dir, "frontier_summary.json"), "w") as f:
            json.dump(frontier_summary, f, indent=2)
    
    def export_execution_summary(self, execution_data):
        """Export execution summary to SMT format"""
        smt_content = "(set-logic ALL)\n"
        
        # 添加元信息
        smt_content += f"; Execution Summary\n"
        smt_content += f"; Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        smt_content += f"; Generated Inputs: {len(execution_data.get('generated_inputs', []))}\n"
        smt_content += f"; Return Values: {execution_data.get('return_values', [])}\n"
        smt_content += f"; Path Length: {len(execution_data.get('branch_trace', []))}\n"
        
        # 写入文件
        with open(os.path.join(self.output_dir, "execution_summary.smt2"), "w") as f:
            f.write(smt_content)
        
        # 同时生成JSON格式的摘要
        execution_summary = {
            "timestamp": time.time(),
            "generated_inputs_count": len(execution_data.get('generated_inputs', [])),
            "return_values": execution_data.get('return_values', []),
            "path_length": len(execution_data.get('branch_trace', [])),
            "branch_trace": execution_data.get('branch_trace', [])
        }
        
        with open(os.path.join(self.output_dir, "execution_summary.json"), "w") as f:
            json.dump(execution_summary, f, indent=2)
