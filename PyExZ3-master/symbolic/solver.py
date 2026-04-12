"""
统一求解器接口 - 基于PyCT优化

这个模块提供了统一的求解器接口，支持多种SMT求解器（Z3, CVC4等），
集成了PyCT的优化功能：错误处理、日志记录、模型解析和统计信息收集。
"""

import logging
import os
import re
import subprocess
import sys
import time
from abc import ABC, abstractmethod

log = logging.getLogger("se.solver")

class SolverError(Exception):
    """求解器相关错误的基类"""
    pass

class SolverTimeout(SolverError):
    """求解器超时错误"""
    pass

class SolverUnsat(SolverError):
    """约束不可满足错误"""
    pass

class SolverUnknown(SolverError):
    """求解器返回未知结果"""
    pass


class UnifiedSolver:
    """
    统一求解器类，整合PyCT的优化功能
    
    功能特点：
    1. 支持多种求解器后端（Z3, CVC4）
    2. 完善的错误处理和日志记录
    3. 模型解析优化
    4. 统计信息收集
    5. 查询存储功能
    """
    
    # 类变量，用于统计和配置
    cnt = 1  # 查询计数器
    stats = {
        'sat_number': 0,
        'sat_time': 0,
        'unsat_number': 0,
        'unsat_time': 0,
        'otherwise_number': 0,
        'otherwise_time': 0
    }
    
    def __init__(self, solver_type='z3', timeout=10, store=None, statsdir=None):
        """
        初始化求解器
        
        Args:
            solver_type: 求解器类型 ('z3', 'cvc4')
            timeout: 求解超时时间（秒）
            store: 存储目录，用于保存SMT2查询文件
            statsdir: 统计目录，用于保存统计信息
        """
        self.solver_type = solver_type.lower()
        self.timeout = timeout
        self.store = store
        self.statsdir = statsdir
        
        # 初始化统计目录
        if self.statsdir:
            os.makedirs(self.statsdir, exist_ok=True)
            os.makedirs(os.path.join(self.statsdir, 'formula'), exist_ok=True)
        
        # 初始化存储目录
        if self.store and not os.path.isdir(self.store):
            if not re.compile(r"^\d+$").match(self.store):
                os.makedirs(self.store, exist_ok=True)
        
        # 配置求解器命令
        self._configure_solver()
        
        log.info(f"Initialized {self.solver_type.upper()} solver with timeout={timeout}s")
    
    def _configure_solver(self):
        """配置求解器命令"""
        if self.solver_type == "cvc4":
            self.cmd = ["cvc4"] + ["--produce-models", "--lang", "smt", "--quiet", "--strings-exp"]
            self.cmd += [f"--tlimit={self.timeout * 1000}"]
        elif self.solver_type == "z3":
            # Z3使用Python API，这里保留命令行接口用于调试
            self.cmd = ["z3", "-in", f"-T:{self.timeout}"]
        else:
            raise NotImplementedError(f"Unsupported solver type: {self.solver_type}")
    
    def solve_from_constraint(self, constraint, engine=None):
        """
        从约束对象求解模型
        
        Args:
            constraint: 路径约束对象
            engine: 探索引擎，用于获取变量类型信息
            
        Returns:
            模型字典或None
        """
        # 构建SMT公式
        smt_formula = self._build_formula_from_constraint(constraint)
        
        # 记录求解开始
        query_id = UnifiedSolver.cnt
        UnifiedSolver.cnt += 1
        
        log.info(f"Solving query {query_id}: {constraint}")
        
        start_time = time.time()
        
        try:
            # 求解
            if self.solver_type == "z3":
                # 使用Python API调用Z3
                model = self._solve_with_z3_api(smt_formula, engine)
            else:
                # 使用命令行调用其他求解器
                model = self._solve_with_cli(smt_formula, engine)
            
            elapsed = time.time() - start_time
            
            # 更新统计信息
            self._update_stats(model, elapsed)
            
            # 保存查询文件（如果启用）
            self._save_query_file(query_id, smt_formula, model)
            
            log.info(f"Query {query_id}: {'SAT' if model else 'UNSAT'} ({elapsed:.3f}s)")
            return model
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.stats['otherwise_number'] += 1
            self.stats['otherwise_time'] += elapsed
            
            log.error(f"Query {query_id} failed: {e}")
            
            # 保存失败的查询
            self._save_query_file(query_id, smt_formula, "ERROR")
            
            raise
    
    def _solve_with_z3_api(self, smt_formula, engine):
        """使用Z3 Python API求解"""
        try:
            from z3 import Solver, parse_smt2_string, sat, unsat
            
            # 创建求解器
            solver = Solver()
            
            # 解析SMT2字符串
            assertions = parse_smt2_string(smt_formula)
            for a in assertions:
                solver.add(a)
            
            # 检查可满足性
            result = solver.check()
            
            if result == sat:
                model = solver.model()
                # 转换为PyExZ3格式的模型
                return self._convert_z3_model(model, engine)
            elif result == unsat:
                return None
            else:
                raise SolverUnknown("Z3 returned unknown")
                
        except ImportError:
            log.warning("Z3 Python API not available, falling back to CLI")
            return self._solve_with_cli(smt_formula, engine)
    
    def _solve_with_cli(self, smt_formula, engine):
        """使用命令行求解器"""
        try:
            completed_process = subprocess.run(
                self.cmd,
                input=smt_formula.encode(),
                capture_output=True,
                timeout=self.timeout + 1  # 比配置的超时多一点
            )
            
            output = completed_process.stdout.decode()
            
            if not output:
                raise SolverError("Solver returned empty output")
            
            lines = output.splitlines()
            status = lines[0].lower() if lines else "unknown"
            
            if "error" in status:
                log.error(f"Solver error: {status}")
                log.error(f"Query: {smt_formula[:500]}...")
                raise SolverError(f"Solver error: {status}")
            
            if "sat" in status:
                model_lines = lines[1:] if len(lines) > 1 else []
                return self._parse_model(model_lines, engine)
            elif "unsat" in status:
                return None
            else:
                raise SolverUnknown(f"Solver returned: {status}")
                
        except subprocess.TimeoutExpired:
            raise SolverTimeout(f"Solver timeout after {self.timeout} seconds")
        except Exception as e:
            raise SolverError(f"CLI solver failed: {e}")
    
    def _build_formula_from_constraint(self, constraint):
        """
        从约束构建SMT公式
        
        注意：这个方法需要与现有的SMT导出器集成
        当前使用简化的实现，实际应使用SMTExporter
        """
        # 这是一个占位符实现
        # 实际应调用SMTExporter.export_path_constraint_smt2()
        
        # 简化的SMT2公式
        smt_formula = """(set-logic QF_BV)
(declare-fun x () Int)
(declare-fun y () Int)
(assert (> x 0))
(assert (< y 10))
(check-sat)
(get-model)"""
        
        return smt_formula
    
    def _parse_model(self, model_lines, engine):
        """解析求解器返回的模型"""
        model = {}
        
        for line in model_lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            # 解析格式: ((var_name value))
            if line.startswith('((') and line.endswith('))'):
                content = line[2:-2]
                parts = content.split(' ', 1)
                if len(parts) == 2:
                    var_name, value_str = parts
                    
                    # 获取变量类型
                    var_type = self._get_var_type(var_name, engine)
                    
                    # 解析值
                    value = self._parse_value(value_str, var_type)
                    
                    model[var_name] = value
        
        return model
    
    def _convert_z3_model(self, z3_model, engine):
        """转换Z3模型为PyExZ3格式"""
        model = {}
        
        for decl in z3_model:
            var_name = str(decl.name())
            
            # 获取变量值
            value_expr = z3_model[decl]
            
            # 获取变量类型
            var_type = self._get_var_type(var_name, engine)
            
            # 转换值
            if var_type == "Bool":
                value = bool(value_expr)
            elif var_type == "Int":
                value = int(str(value_expr))
            elif var_type == "Real":
                value = float(str(value_expr))
            else:
                # 默认为字符串
                value = str(value_expr)
            
            model[var_name] = value
        
        return model
    
    def _get_var_type(self, var_name, engine):
        """获取变量类型"""
        if engine and hasattr(engine, 'var_to_types'):
            return engine.var_to_types.get(var_name, "Int")
        return "Int"
    
    def _parse_value(self, value_str, var_type):
        """根据类型解析值字符串"""
        try:
            if var_type == "Bool":
                if value_str == 'true':
                    return True
                elif value_str == 'false':
                    return False
                else:
                    raise ValueError(f"Invalid boolean value: {value_str}")
            
            elif var_type == "Real":
                # 处理负数格式: (- 3.14)
                if value_str.startswith('(') and ' ' in value_str:
                    # 格式: (- 3.14)
                    parts = value_str[1:-1].split()
                    if len(parts) == 2 and parts[0] == '-':
                        return -float(parts[1])
                return float(value_str)
            
            elif var_type == "Int":
                # 处理负数格式: (- 42)
                if value_str.startswith('(') and ' ' in value_str:
                    # 格式: (- 42)
                    parts = value_str[1:-1].split()
                    if len(parts) == 2 and parts[0] == '-':
                        return -int(parts[1])
                return int(value_str)
            
            else:
                # 字符串类型，移除引号
                if value_str.startswith('"') and value_str.endswith('"'):
                    return value_str[1:-1]
                return value_str
                
        except Exception as e:
            log.warning(f"Failed to parse value '{value_str}' as {var_type}: {e}")
            return value_str
    
    def _update_stats(self, model, elapsed):
        """更新统计信息"""
        if model is not None:
            UnifiedSolver.stats['sat_number'] += 1
            UnifiedSolver.stats['sat_time'] += elapsed
        else:
            UnifiedSolver.stats['unsat_number'] += 1
            UnifiedSolver.stats['unsat_time'] += elapsed
    
    def _save_query_file(self, query_id, formula, result):
        """保存查询文件"""
        if not self.store and not self.statsdir:
            return
        
        status = "SAT" if result else "UNSAT" if result is None else "ERROR"
        
        # 保存到存储目录
        if self.store:
            if re.compile(r"^\d+$").match(self.store):
                # 存储为固定文件名
                if int(self.store) == query_id:
                    filename = f"{self.store}_{status}.smt2"
                    with open(filename, 'w') as f:
                        f.write(formula)
            else:
                # 存储到目录
                filename = os.path.join(self.store, f"{query_id}_{status}.smt2")
                with open(filename, 'w') as f:
                    f.write(formula)
        
        # 保存到统计目录
        if self.statsdir:
            filename = os.path.join(self.statsdir, 'formula', f"{query_id}_{status}.smt2")
            with open(filename, 'w') as f:
                f.write(formula)
    
    @classmethod
    def get_stats(cls):
        """获取统计信息"""
        return cls.stats.copy()
    
    @classmethod
    def reset_stats(cls):
        """重置统计信息"""
        cls.stats = {
            'sat_number': 0,
            'sat_time': 0,
            'unsat_number': 0,
            'unsat_time': 0,
            'otherwise_number': 0,
            'otherwise_time': 0
        }
        cls.cnt = 1


# 向后兼容的包装器
class SolverWrapper:
    """
    向后兼容的求解器包装器
    
    为现有的Z3Wrapper和CVCWrapper提供统一接口
    """
    
    def __init__(self, solver_type='z3', **kwargs):
        self.solver = UnifiedSolver(solver_type=solver_type, **kwargs)
        self.solver_type = solver_type
    
    def findCounterexample(self, asserts, query):
        """
        向后兼容的接口
        
        Args:
            asserts: 断言列表
            query: 查询表达式
            
        Returns:
            反例模型或None
        """
        # 注意：这里需要将PyExZ3的断言和查询转换为约束对象
        # 这是一个简化的实现
        
        # 创建模拟约束对象
        class MockConstraint:
            def __init__(self, asserts, query):
                self.asserts = asserts
                self.query = query
        
        constraint = MockConstraint(asserts, query)
        
        try:
            return self.solver.solve_from_constraint(constraint)
        except SolverUnsat:
            return None
        except Exception as e:
            log.error(f"求解失败: {e}")
            return None


# 配置日志记录
def setup_logging():
    """配置SMTLIB2日志级别"""
    # 添加SMTLIB2日志级别
    SMTLIB2_LEVEL_NUM = 25
    logging.addLevelName(SMTLIB2_LEVEL_NUM, "SMTLIB2")
    
    def smtlib2(self, message, *args, **kwargs):
        if self.isEnabledFor(SMTLIB2_LEVEL_NUM):
            self._log(SMTLIB2_LEVEL_NUM, message, args, **kwargs)
    
    logging.Logger.smtlib2 = smtlib2


# 初始化时设置日志
setup_logging()