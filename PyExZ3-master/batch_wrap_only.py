#!/usr/bin/env python3
"""
批量包装学生代码脚本
只对 student_code 文件夹中的所有文件进行包装，不执行符号执行
"""

import os
import sys
import time
from pathlib import Path

# 配置
STUDENT_CODE_DIR = r'e:\Graduation_Projection\PyExZ3-master\student_code'
WRAPPED_DIR = r'e:\Graduation_Projection\PyExZ3-master\student_code_wrapped'
REPORT_FILE = r'e:\Graduation_Projection\PyExZ3-master\batch_wrap_report.txt'

# 测试配置
USE_ENHANCED_WRAPPER = True  # 是否使用增强包装器

def create_dirs():
    """创建必要的目录"""
    os.makedirs(WRAPPED_DIR, exist_ok=True)

def wrap_code_file(input_file, output_file, use_enhanced=True):
    """使用包装器包装单个文件"""
    import subprocess
    
    if use_enhanced:
        cmd = [
            sys.executable,
            'enhanced_student_wrapper.py',
            input_file,
            '-o', output_file,
            '--no-analysis'
        ]
    else:
        cmd = [
            sys.executable,
            'student_code_wrapper.py',
            input_file,
            '-o', output_file,
            '--no-analysis'
        ]

    try:
        result = subprocess.run(
            cmd,
            cwd=r'e:\Graduation_Projection\PyExZ3-master',
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "包装超时"
    except Exception as e:
        return False, "", str(e)

def main():
    print("=" * 70)
    print("PyExZ3 批量学生代码包装")
    print("=" * 70)

    # 创建目录
    create_dirs()

    # 获取所有 Python 文件
    student_files = list(Path(STUDENT_CODE_DIR).glob('*.py'))
    print(f"\n找到 {len(student_files)} 个学生代码文件")
    print(f"包装器: {'增强包装器' if USE_ENHANCED_WRAPPER else '基础包装器'}")

    if not student_files:
        print("错误：没有找到任何学生代码文件！")
        return

    # 统计变量
    results = {
        'total': len(student_files),
        'wrap_success': 0,
        'wrap_failed': 0,
        'details': []
    }

    start_time = time.time()

    for i, student_file in enumerate(sorted(student_files), 1):
        filename = student_file.name
        print(f"\n[{i}/{results['total']}] {filename}")
        print("    " + "-" * 50)

        wrapped_file = Path(WRAPPED_DIR) / filename

        success, stdout, stderr = wrap_code_file(
            str(student_file),
            str(wrapped_file),
            USE_ENHANCED_WRAPPER
        )

        if success:
            results['wrap_success'] += 1
            print(f"    [OK] 包装成功")
            results['details'].append({
                'file': filename,
                'wrap_success': True
            })
        else:
            results['wrap_failed'] += 1
            print(f"    [FAIL] 包装失败: {stderr[:100]}")
            results['details'].append({
                'file': filename,
                'wrap_success': False,
                'error': stderr
            })

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("包装完成！")
    print("=" * 70)

    total = results['total']
    print(f"\n总计: {total} 个文件")
    print(f"包装成功: {results['wrap_success']} 个")
    print(f"包装失败: {results['wrap_failed']} 个")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"平均耗时: {elapsed_time / total:.2f} 秒/文件")

    success_rate = results['wrap_success'] / total * 100 if total > 0 else 0
    print(f"成功率: {success_rate:.1f}%")

    # 写入报告文件
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("PyExZ3 批量学生代码包装报告\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"包装时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"源目录: {STUDENT_CODE_DIR}\n")
        f.write(f"目标目录: {WRAPPED_DIR}\n")
        f.write(f"包装器: {'增强包装器' if USE_ENHANCED_WRAPPER else '基础包装器'}\n\n")

        f.write("=" * 70 + "\n")
        f.write("统计结果\n")
        f.write("=" * 70 + "\n")
        f.write(f"总计: {total} 个文件\n")
        f.write(f"包装成功: {results['wrap_success']} 个\n")
        f.write(f"包装失败: {results['wrap_failed']} 个\n")
        f.write(f"成功率: {success_rate:.1f}%\n")
        f.write(f"总耗时: {elapsed_time:.2f} 秒\n\n")

        if results['wrap_failed'] > 0:
            f.write("\n" + "=" * 70 + "\n")
            f.write("失败详情\n")
            f.write("=" * 70 + "\n")
            for detail in results['details']:
                if not detail['wrap_success']:
                    f.write(f"\n{detail['file']}:\n")
                    f.write(f"  错误: {detail.get('error', 'unknown')}\n")

    print(f"\n报告已保存到: {REPORT_FILE}")
    print(f"包装后的文件保存在: {WRAPPED_DIR}")

if __name__ == '__main__':
    main()
