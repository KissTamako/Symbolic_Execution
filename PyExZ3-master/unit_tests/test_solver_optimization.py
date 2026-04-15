import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from symbolic.z3_wrap import Z3Wrapper

class TestSolverOptimization(unittest.TestCase):
    """测试求解器优化功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.solver = Z3Wrapper()
    
    def test_unsat_cache_initialization(self):
        """测试UNSAT缓存初始化"""
        self.assertEqual(len(self.solver.unsat_cache), 0)
        self.assertEqual(self.solver.stats['total_calls'], 0)
        self.assertEqual(self.solver.stats['cache_hits'], 0)
        self.assertEqual(self.solver.stats['cache_misses'], 0)
    
    def test_stats_initialization(self):
        """测试性能统计初始化"""
        stats = self.solver.getStats()
        self.assertEqual(stats['total_calls'], 0)
        self.assertEqual(stats['cache_hits'], 0)
        self.assertEqual(stats['cache_misses'], 0)
    
    def test_stats_reset(self):
        """测试性能统计重置"""
        # 先修改一些统计值
        self.solver.stats['total_calls'] = 10
        self.solver.stats['cache_hits'] = 5
        self.solver.stats['cache_misses'] = 5
        
        # 重置统计
        self.solver.resetStats()
        
        # 检查是否重置成功
        stats = self.solver.getStats()
        self.assertEqual(stats['total_calls'], 0)
        self.assertEqual(stats['cache_hits'], 0)
        self.assertEqual(stats['cache_misses'], 0)
    
    def test_get_constraint_key(self):
        """测试约束键生成（简化测试）"""
        # 这个测试比较复杂，因为需要实际的Constraint对象
        # 这里我们只测试方法是否存在
        self.assertTrue(hasattr(self.solver, '_getConstraintKey'))
    
    def test_get_stats(self):
        """测试获取性能统计"""
        stats = self.solver.getStats()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_calls', stats)
        self.assertIn('cache_hits', stats)
        self.assertIn('cache_misses', stats)

if __name__ == '__main__':
    unittest.main()
