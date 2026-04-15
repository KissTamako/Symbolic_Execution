import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from symbolic.z3_wrap import Z3Wrapper
from symbolic.explore import ExplorationEngine
from symbolic.invocation import FunctionInvocation
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)

class TestUNSATCache(unittest.TestCase):
    """测试UNSAT缓存功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.solver = Z3Wrapper()
    
    def test_unsat_cache_initialization(self):
        """测试UNSAT缓存初始化"""
        self.assertEqual(len(self.solver.unsat_cache), 0)
        self.assertEqual(self.solver.stats['total_calls'], 0)
        self.assertEqual(self.solver.stats['cache_hits'], 0)
        self.assertEqual(self.solver.stats['cache_misses'], 0)
    
    def test_stats_methods(self):
        """测试统计方法"""
        # 测试getStats
        stats = self.solver.getStats()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_calls', stats)
        self.assertIn('cache_hits', stats)
        self.assertIn('cache_misses', stats)
        
        # 测试resetStats
        self.solver.stats['total_calls'] = 10
        self.solver.resetStats()
        self.assertEqual(self.solver.stats['total_calls'], 0)
    
    def test_get_constraint_key_exists(self):
        """测试约束键生成方法存在"""
        self.assertTrue(hasattr(self.solver, '_getConstraintKey'))

if __name__ == '__main__':
    unittest.main()
