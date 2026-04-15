import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from symbolic.normalizer import ConstraintNormalizer

class TestConstraintNormalizer(unittest.TestCase):
    """测试约束规范化模块"""
    
    def setUp(self):
        """设置测试环境"""
        self.normalizer = ConstraintNormalizer()
    
    def test_variable_renaming(self):
        """测试变量重命名功能"""
        test_cases = [
            ('a', 'ARG0'),
            ('b', 'ARG1'),
            ('c', 'ARG2'),
            ('x', 'ARG0'),
            ('y', 'ARG1'),
            ('z', 'ARG2'),
            ('arg0', 'arg0'),  # 不在映射表中的变量
        ]
        
        for input_var, expected in test_cases:
            result = self.normalizer._rename_variable(input_var)
            self.assertEqual(result, expected)
    
    def test_expression_normalization(self):
        """测试表达式标准化功能"""
        # 测试交换律操作的排序
        expr1 = ['+', 'b', 'a']
        normalized1 = self.normalizer.normalize_expression(expr1)
        self.assertEqual(normalized1, ['+', 'a', 'b'])
        
        # 测试比较操作的方向规范化
        expr2 = ['>', 'x', 5]
        normalized2 = self.normalizer.normalize_expression(expr2)
        self.assertEqual(normalized2, ['<', 5, 'x'])
        
        # 测试常量合并
        expr3 = ['+', 1, 2, 'x']
        normalized3 = self.normalizer.normalize_expression(expr3)
        self.assertEqual(normalized3, ['+', 3, 'x'])
    
    def test_constant_merging(self):
        """测试常量合并功能"""
        # 测试加法常量合并
        args1 = [1, 2, 3, 'x']
        merged1 = self.normalizer._merge_constants('+', args1)
        self.assertEqual(merged1, ['+', 6, 'x'])
        
        # 测试乘法常量合并
        args2 = [2, 3, 4, 'x']
        merged2 = self.normalizer._merge_constants('*', args2)
        self.assertEqual(merged2, ['*', 24, 'x'])
        
        # 测试只有常量的情况
        args3 = [1, 2, 3]
        merged3 = self.normalizer._merge_constants('+', args3)
        self.assertEqual(merged3, 6)
    
    def test_comparison_normalization(self):
        """测试比较操作的方向规范化"""
        # 测试大于操作
        result1 = self.normalizer._normalize_comparison('>', ['x', 5])
        self.assertEqual(result1, ['<', 5, 'x'])
        
        # 测试大于等于操作
        result2 = self.normalizer._normalize_comparison('>=', ['x', 5])
        self.assertEqual(result2, ['<=', 5, 'x'])
        
        # 测试小于操作（不需要转换）
        result3 = self.normalizer._normalize_comparison('<', ['x', 5])
        self.assertEqual(result3, ['<', 'x', 5])
        
        # 测试小于等于操作（不需要转换）
        result4 = self.normalizer._normalize_comparison('<=', ['x', 5])
        self.assertEqual(result4, ['<=', 'x', 5])

if __name__ == '__main__':
    unittest.main()
