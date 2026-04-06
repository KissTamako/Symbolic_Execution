#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教学反馈生成器
面向学生代码的增强型符号执行工具 - 教学反馈模块

功能：
1. 基于代码分析和测试结果生成教学反馈
2. 提供针对性的改进建议
3. 生成分数和评价等级
4. 输出格式化的反馈报告
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class TeachingFeedbackGenerator:
    """教学反馈生成器"""
    
    def __init__(self):
        self.feedback_templates = self._load_feedback_templates()
    
    def _load_feedback_templates(self) -> Dict[str, Dict[str, str]]:
        """加载反馈模板"""
        return {
            'code_quality': {
                'high': "代码结构清晰，函数设计合理，符合Python编码规范。",
                'medium': "代码结构基本清晰，但部分地方可以进一步优化。",
                'low': "代码结构需要改进，建议重新组织逻辑并添加注释。"
            },
            'error_handling': {
                'high': "异常处理得当，考虑了边界情况和错误输入。",
                'medium': "基本异常处理，但可以考虑更多边界情况。",
                'low': "缺乏异常处理，可能在某些输入下出现错误。"
            },
            'efficiency': {
                'high': "算法效率高，时间复杂度合理。",
                'medium': "算法效率基本可接受，但存在优化空间。",
                'low': "算法效率有待提高，存在不必要的复杂度。"
            },
            'test_coverage': {
                'high': "符号执行测试覆盖全面，所有路径都被探索。",
                'medium': "符号执行测试覆盖基本路径，但可能存在遗漏。",
                'low': "符号执行测试覆盖不足，建议增加测试用例。"
            },
            'correctness': {
                'high': "代码逻辑正确，所有测试用例均通过。",
                'medium': "代码基本正确，但存在一些边界情况问题。",
                'low': "代码存在逻辑错误，部分测试用例未通过。"
            }
        }
    
    def generate_feedback(self, analysis_result: Dict[str, Any], 
                         test_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成完整教学反馈
        
        Args:
            analysis_result: 代码分析结果
            test_result: 符号执行测试结果
            
        Returns:
            包含完整反馈信息的字典
        """
        # 计算各项得分
        scores = self._calculate_scores(analysis_result, test_result)
        
        # 生成评语
        comments = self._generate_comments(scores, analysis_result, test_result)
        
        # 生成改进建议
        suggestions = self._generate_suggestions(analysis_result, test_result)
        
        # 生成总体评价
        overall_evaluation = self._generate_overall_evaluation(scores)
        
        feedback = {
            'student_info': {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'code_type': analysis_result.get('code_type', 'unknown'),
                'original_file': analysis_result.get('original_file', 'unknown')
            },
            'scores': scores,
            'comments': comments,
            'suggestions': suggestions,
            'overall_evaluation': overall_evaluation,
            'analysis_summary': {
                'features': analysis_result.get('features', {}),
                'test_results': {
                    'success': test_result.get('success', False),
                    'test_passed': test_result.get('test_passed', False),
                    'paths_explored': test_result.get('paths_explored', 0),
                    'execution_time': test_result.get('execution_time', 0)
                }
            }
        }
        
        return feedback
    
    def _calculate_scores(self, analysis_result: Dict[str, Any], 
                         test_result: Dict[str, Any]) -> Dict[str, float]:
        """计算各项得分（0-100分）"""
        scores = {}
        
        # 1. 代码质量得分（基于代码特征）
        features = analysis_result.get('features', {})
        
        # 函数设计得分
        function_count = features.get('function_count', 0)
        has_main = features.get('has_main_function', False)
        has_docstring = any(f.get('has_docstring', False) for f in features.get('functions', []))
        
        function_score = 0
        if function_count >= 2:
            function_score = 80
            if has_main:
                function_score += 10
            if has_docstring:
                function_score += 10
        elif function_count == 1:
            function_score = 60
        else:
            function_score = 40
        
        scores['code_structure'] = min(100, function_score)
        
        # 2. 错误处理得分
        error_count = features.get('error_count', 0)
        try_count = features.get('try_count', 0)
        input_count = features.get('input_call_count', 0)
        
        error_handling_score = 70  # 基础分
        
        if error_count == 0:
            error_handling_score += 10
        
        if input_count > 0 and try_count > 0:
            error_handling_score += 20
        elif input_count == 0:
            error_handling_score += 10
        
        scores['error_handling'] = min(100, error_handling_score)
        
        # 3. 算法效率得分
        max_nesting = features.get('max_nesting_depth', 0)
        loop_count = features.get('loop_count', 0)
        
        efficiency_score = 80  # 基础分
        
        if max_nesting <= 3:
            efficiency_score += 10
        
        if loop_count <= 2:
            efficiency_score += 10
        elif loop_count > 4:
            efficiency_score -= 15
        
        scores['efficiency'] = min(100, efficiency_score)
        
        # 4. 测试覆盖得分
        test_passed = test_result.get('test_passed', False)
        paths_explored = test_result.get('paths_explored', 0)
        success = test_result.get('success', False)
        
        test_coverage_score = 0
        
        if success:
            test_coverage_score = 60
            if test_passed:
                test_coverage_score += 30
            if paths_explored >= 3:
                test_coverage_score += 10
        
        scores['test_coverage'] = min(100, test_coverage_score)
        
        # 5. 正确性得分
        correctness_score = 0
        
        if test_passed:
            correctness_score = 90
            if paths_explored >= 2:
                correctness_score = 100
        elif success:
            correctness_score = 50
        else:
            correctness_score = 20
        
        scores['correctness'] = correctness_score
        
        # 计算总分
        weights = {
            'code_structure': 0.15,
            'error_handling': 0.15,
            'efficiency': 0.20,
            'test_coverage': 0.20,
            'correctness': 0.30
        }
        
        total_score = sum(scores[category] * weight 
                         for category, weight in weights.items())
        scores['total'] = round(total_score, 1)
        
        return scores
    
    def _generate_comments(self, scores: Dict[str, float], 
                          analysis_result: Dict[str, Any],
                          test_result: Dict[str, Any]) -> Dict[str, str]:
        """生成各项评语"""
        comments = {}
        
        # 根据得分选择评语模板
        for category in ['code_structure', 'error_handling', 'efficiency', 
                        'test_coverage', 'correctness']:
            score = scores[category]
            
            if score >= 80:
                level = 'high'
            elif score >= 60:
                level = 'medium'
            else:
                level = 'low'
            
            # 获取模板评语
            template_comment = self.feedback_templates.get(category, {}).get(level, "")
            
            # 添加具体细节
            detail_comment = self._add_specific_details(category, analysis_result, test_result)
            
            comments[category] = f"{template_comment} {detail_comment}".strip()
        
        return comments
    
    def _add_specific_details(self, category: str, 
                             analysis_result: Dict[str, Any],
                             test_result: Dict[str, Any]) -> str:
        """添加具体细节到评语"""
        features = analysis_result.get('features', {})
        
        if category == 'code_structure':
            function_count = features.get('function_count', 0)
            if function_count == 0:
                return "代码未使用函数封装，建议将逻辑封装到函数中。"
            elif function_count == 1:
                return f"定义了1个函数，建议考虑是否需要更多辅助函数。"
            else:
                return f"定义了{function_count}个函数，函数设计合理。"
        
        elif category == 'error_handling':
            input_count = features.get('input_call_count', 0)
            try_count = features.get('try_count', 0)
            
            if input_count > 0 and try_count == 0:
                return "代码使用input()获取用户输入，但未添加异常处理。"
            elif input_count > 0 and try_count > 0:
                return "代码包含输入验证和异常处理，安全性较好。"
            else:
                return "代码未涉及外部输入，无需复杂异常处理。"
        
        elif category == 'efficiency':
            max_nesting = features.get('max_nesting_depth', 0)
            loop_count = features.get('loop_count', 0)
            
            details = []
            if max_nesting > 3:
                details.append(f"最大嵌套深度为{max_nesting}，可能影响可读性")
            if loop_count > 3:
                details.append(f"循环数量为{loop_count}，可考虑优化")
            
            if details:
                return f"注意: {'; '.join(details)}。"
            else:
                return "代码复杂度控制得当。"
        
        elif category == 'test_coverage':
            paths_explored = test_result.get('paths_explored', 0)
            test_passed = test_result.get('test_passed', False)
            
            if not test_result.get('success', False):
                return "符号执行测试未成功运行。"
            elif paths_explored == 0:
                return "符号执行未探索到任何路径。"
            elif paths_explored == 1:
                return f"符号执行探索了{paths_explored}条路径，覆盖有限。"
            else:
                return f"符号执行探索了{paths_explored}条路径，覆盖较好。"
        
        elif category == 'correctness':
            test_passed = test_result.get('test_passed', False)
            success = test_result.get('success', False)
            
            if not success:
                return "测试执行失败，无法验证正确性。"
            elif test_passed:
                return "所有测试用例通过，代码逻辑正确。"
            else:
                return "部分测试用例未通过，代码可能存在逻辑错误。"
        
        return ""
    
    def _generate_suggestions(self, analysis_result: Dict[str, Any],
                             test_result: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        features = analysis_result.get('features', {})
        
        # 1. 代码结构建议
        if features.get('function_count', 0) == 0:
            suggestions.append("建议将代码逻辑封装到函数中，提高代码复用性。")
        
        if features.get('has_global_code', False) and features.get('function_count', 0) > 0:
            suggestions.append("建议将全局代码移到main()函数中，保持代码结构清晰。")
        
        # 2. 错误处理建议
        if features.get('input_call_count', 0) > 0 and features.get('try_count', 0) == 0:
            suggestions.append("建议为input()调用添加try-except异常处理。")
        
        # 3. 效率建议
        if features.get('max_nesting_depth', 0) > 3:
            suggestions.append("代码嵌套过深，建议提取部分逻辑为独立函数。")
        
        if features.get('loop_count', 0) > 3:
            suggestions.append("循环数量较多，建议考虑算法优化。")
        
        # 4. 测试相关建议
        if not test_result.get('success', False):
            suggestions.append("符号执行测试失败，请检查代码语法和依赖。")
        elif test_result.get('paths_explored', 0) < 2:
            suggestions.append("符号执行覆盖路径较少，建议增加测试用例或调整代码逻辑。")
        
        # 5. 从分析结果中提取建议
        original_suggestions = analysis_result.get('recommendations', [])
        suggestions.extend(original_suggestions[:3])  # 最多取3条
        
        # 去重
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion not in unique_suggestions:
                unique_suggestions.append(suggestion)
        
        return unique_suggestions[:5]  # 最多返回5条建议
    
    def _generate_overall_evaluation(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """生成总体评价"""
        total_score = scores['total']
        
        if total_score >= 90:
            grade = "优秀"
            evaluation = "代码质量很高，逻辑清晰，测试覆盖全面。"
        elif total_score >= 80:
            grade = "良好"
            evaluation = "代码质量良好，有少量改进空间。"
        elif total_score >= 70:
            grade = "中等"
            evaluation = "代码质量一般，需要进一步优化和改进。"
        elif total_score >= 60:
            grade = "及格"
            evaluation = "代码基本功能实现，但存在较多改进空间。"
        else:
            grade = "不及格"
            evaluation = "代码需要大幅改进，建议重新设计和实现。"
        
        # 生成优点和不足
        strengths = []
        weaknesses = []
        
        for category in ['code_structure', 'error_handling', 'efficiency', 
                        'test_coverage', 'correctness']:
            score = scores[category]
            if score >= 80:
                strengths.append(category.replace('_', ' '))
            elif score < 60:
                weaknesses.append(category.replace('_', ' '))
        
        return {
            'total_score': total_score,
            'grade': grade,
            'evaluation': evaluation,
            'strengths': strengths,
            'weaknesses': weaknesses
        }
    
    def format_feedback_report(self, feedback: Dict[str, Any], 
                              output_format: str = 'text') -> str:
        """格式化反馈报告"""
        if output_format == 'json':
            return json.dumps(feedback, ensure_ascii=False, indent=2)
        
        # 文本格式
        report = []
        
        # 标题
        report.append("=" * 70)
        report.append("学生代码教学反馈报告")
        report.append("=" * 70)
        
        # 学生信息
        student_info = feedback['student_info']
        report.append(f"评估时间: {student_info['timestamp']}")
        report.append(f"代码类型: {student_info['code_type']}")
        report.append(f"原始文件: {student_info.get('original_file', 'N/A')}")
        report.append("")
        
        # 总体评价
        overall = feedback['overall_evaluation']
        report.append(f"总分: {overall['total_score']:.1f}/100")
        report.append(f"等级: {overall['grade']}")
        report.append(f"评价: {overall['evaluation']}")
        report.append("")
        
        # 各维度得分
        report.append("各维度得分:")
        report.append("-" * 40)
        
        categories = {
            'code_structure': '代码结构',
            'error_handling': '错误处理',
            'efficiency': '算法效率',
            'test_coverage': '测试覆盖',
            'correctness': '代码正确性'
        }
        
        for eng_name, chi_name in categories.items():
            score = feedback['scores'][eng_name]
            bar = "█" * int(score / 5)  # 每5分一个方块
            report.append(f"{chi_name:12} {score:6.1f}/100 {bar}")
        
        report.append("")
        
        # 详细评语
        report.append("详细评语:")
        report.append("-" * 40)
        
        for eng_name, chi_name in categories.items():
            comment = feedback['comments'][eng_name]
            report.append(f"{chi_name}: {comment}")
            report.append("")
        
        # 改进建议
        suggestions = feedback['suggestions']
        if suggestions:
            report.append("改进建议:")
            report.append("-" * 40)
            for i, suggestion in enumerate(suggestions, 1):
                report.append(f"{i}. {suggestion}")
            report.append("")
        
        # 优点和不足
        strengths = overall['strengths']
        weaknesses = overall['weaknesses']
        
        if strengths:
            report.append("优点:")
            report.append("-" * 40)
            for strength in strengths:
                report.append(f"• {strength}")
            report.append("")
        
        if weaknesses:
            report.append("需要改进的方面:")
            report.append("-" * 40)
            for weakness in weaknesses:
                report.append(f"• {weakness}")
            report.append("")
        
        # 分析摘要
        analysis = feedback['analysis_summary']
        report.append("分析摘要:")
        report.append("-" * 40)
        
        features = analysis['features']
        test_results = analysis['test_results']
        
        report.append(f"函数数量: {features.get('function_count', 0)}")
        report.append(f"循环数量: {features.get('loop_count', 0)}")
        report.append(f"条件数量: {features.get('if_count', 0)}")
        report.append(f"最大嵌套深度: {features.get('max_nesting_depth', 0)}")
        report.append(f"输入调用: {features.get('input_call_count', 0)}")
        report.append("")
        report.append(f"测试成功: {'是' if test_results['success'] else '否'}")
        report.append(f"测试通过: {'是' if test_results['test_passed'] else '否'}")
        report.append(f"探索路径: {test_results['paths_explored']}")
        report.append(f"执行时间: {test_results['execution_time']:.2f}秒")
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)


# ========== 使用示例和测试 ==========

def generate_example_feedback():
    """生成示例反馈"""
    print("教学反馈生成器示例")
    print("=" * 60)
    
    # 模拟分析结果
    example_analysis = {
        'success': True,
        'code_type': 'prime_palindrome',
        'features': {
            'function_count': 2,
            'has_main_function': False,
            'functions': [
                {'name': 'sushu', 'has_docstring': False, 'has_return': True},
                {'name': 'huiwenshu', 'has_docstring': False, 'has_return': True}
            ],
            'loop_count': 2,
            'if_count': 3,
            'max_nesting_depth': 3,
            'input_call_count': 1,
            'try_count': 0,
            'error_count': 0,
            'has_global_code': True
        },
        'recommendations': [
            "代码包含全局执行语句，建议将逻辑移到main()函数中",
            "input()调用缺少异常处理，建议添加try-except块"
        ]
    }
    
    # 模拟测试结果
    example_test = {
        'success': True,
        'test_passed': True,
        'paths_explored': 3,
        'execution_time': 0.25
    }
    
    # 生成反馈
    generator = TeachingFeedbackGenerator()
    feedback = generator.generate_feedback(example_analysis, example_test)
    
    # 输出报告
    report = generator.format_feedback_report(feedback)
    print(report)
    
    # 保存JSON格式报告
    json_report = generator.format_feedback_report(feedback, 'json')
    with open("example_feedback_report.json", 'w', encoding='utf-8') as f:
        f.write(json_report)
    print("JSON格式报告已保存到: example_feedback_report.json")
    
    return feedback


def test_integration():
    """测试与现有组件的集成"""
    print("\n" + "=" * 60)
    print("测试与现有组件集成")
    print("=" * 60)
    
    try:
        # 导入现有组件
        from universal_code_analyzer import UniversalCodeAnalyzer
        from enhanced_test_runner import EnhancedTestRunner
        
        # 示例代码
        example_code = '''
def sushu(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def huiwenshu(n):
    return str(n) == str(n)[::-1]

n = int(input("请输入N: "))
result = []
for i in range(2, n+1):
    if sushu(i) and huiwenshu(i):
        result.append(i)
print(result)
'''
        
        # 1. 代码分析
        print("1. 代码分析...")
        analyzer = UniversalCodeAnalyzer(example_code)
        analysis_result = analyzer.analyze()
        
        if not analysis_result['success']:
            print(f"分析失败: {analysis_result.get('error', '未知错误')}")
            return
        
        print(f"   代码类型: {analysis_result['code_type']}")
        print(f"   函数数量: {analysis_result['features']['function_count']}")
        
        # 2. 生成适配器
        print("2. 生成适配器...")
        from universal_adapter_generator import UniversalAdapterGenerator
        
        adapter_generator = UniversalAdapterGenerator(example_code)
        adapter_result = adapter_generator.generate_adapter()
        
        if not adapter_result['success']:
            print(f"生成适配器失败: {adapter_result.get('error', '未知错误')}")
            return
        
        # 保存适配器
        adapter_file = "integration_test_adapter.py"
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.write(adapter_result['adapter_code'])
        print(f"   适配器已保存到: {adapter_file}")
        
        # 3. 符号执行测试
        print("3. 符号执行测试...")
        test_runner = EnhancedTestRunner()
        test_result = test_runner.run_test(adapter_file, max_iters=3)
        
        print(f"   测试成功: {test_result['success']}")
        print(f"   测试通过: {test_result['test_passed']}")
        print(f"   探索路径: {test_result['paths_explored']}")
        
        # 4. 生成教学反馈
        print("4. 生成教学反馈...")
        feedback_generator = TeachingFeedbackGenerator()
        feedback = feedback_generator.generate_feedback(analysis_result, test_result)
        
        # 输出反馈摘要
        overall = feedback['overall_evaluation']
        print(f"   总分: {overall['total_score']:.1f}/100")
        print(f"   等级: {overall['grade']}")
        
        # 5. 保存完整报告
        report = feedback_generator.format_feedback_report(feedback)
        report_file = "integration_test_feedback.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"   完整报告已保存到: {report_file}")
        
        # 清理
        import os
        if os.path.exists(adapter_file):
            os.remove(adapter_file)
            print(f"   清理适配器文件: {adapter_file}")
        
        print("\n集成测试完成！")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保所有依赖组件都存在。")
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    # 生成示例反馈
    generate_example_feedback()
    
    # 测试集成
    test_integration()