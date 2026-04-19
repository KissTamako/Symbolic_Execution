#!/usr/bin/env python3
"""
Batch Student Code Test Script v2
Add timeout mechanism and iteration limit to prevent recursion depth issues
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Configuration
STUDENT_CODE_DIR = r'e:\Graduation_Projection\PyExZ3-master\student_code'
WRAPPED_DIR = r'e:\Graduation_Projection\PyExZ3-master\student_code_wrapped'
REPORT_FILE = r'e:\Graduation_Projection\PyExZ3-master\batch_test_report_v2.txt'

# Test Configuration
USE_ENHANCED_WRAPPER = True
MAX_ITER_PER_FILE = 20
EXEC_TIMEOUT = 20
WRAP_TIMEOUT = 10

# Export Configuration
ENABLE_SIMPLIFY = True
DUMP_CONSTRAINTS = True
DUMP_TRACE = True
DUMP_SEMANTICS = True
DUMP_ALL_EXECUTIONS = True

def create_dirs():
    os.makedirs(WRAPPED_DIR, exist_ok=True)

def wrap_code_file(input_file, output_file, use_enhanced=True):
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
            timeout=WRAP_TIMEOUT
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Wrap timeout"
    except Exception as e:
        return False, "", str(e)

def run_symbolic_execution(wrapped_file, max_iters=20):
    cmd = [
        sys.executable,
        'pyexz3.py',
        '--mode=script',
        f'--max-iters={max_iters}',
        wrapped_file
    ]

    if ENABLE_SIMPLIFY:
        cmd.append('--enable-simplify')
    if DUMP_CONSTRAINTS:
        cmd.append('--dump-constraints')
    if DUMP_TRACE:
        cmd.append('--dump-trace')
    if DUMP_SEMANTICS:
        cmd.append('--dump-semantics')
    if DUMP_ALL_EXECUTIONS:
        cmd.append('--dump-all-executions')

    try:
        result = subprocess.run(
            cmd,
            cwd=r'e:\Graduation_Projection\PyExZ3-master',
            capture_output=True,
            text=True,
            timeout=EXEC_TIMEOUT
        )
        return result.returncode == 0, result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return False, "", "Symbolic execution timeout", -1
    except Exception as e:
        return False, "", str(e), -1

def parse_output(stdout):
    path_count = stdout.count('Input:') + stdout.count('输入:')
    return path_count

def main():
    print("=" * 70)
    print("PyExZ3 Batch Student Code Test v2")
    print("(With timeout protection and iteration limit)")
    print("=" * 70)

    create_dirs()

    student_files = list(Path(STUDENT_CODE_DIR).glob('*.py'))
    print(f"\nFound {len(student_files)} student code files")
    print(f"Config: max_iter={MAX_ITER_PER_FILE}, timeout={EXEC_TIMEOUT}s")
    print(f"Export: simplify={ENABLE_SIMPLIFY}, constraints={DUMP_CONSTRAINTS}, ")
    print(f"      trace={DUMP_TRACE}, semantics={DUMP_SEMANTICS}, all_exec={DUMP_ALL_EXECUTIONS}\n")

    if not student_files:
        print("Error: No student code files found!")
        return

    results = {
        'total': len(student_files),
        'wrap_success': 0,
        'wrap_failed': 0,
        'exec_success': 0,
        'exec_failed': 0,
        'exec_timeout': 0,
        'details': []
    }

    start_time = time.time()

    for i, student_file in enumerate(student_files, 1):
        filename = student_file.name
        wrapped_file = os.path.join(WRAPPED_DIR, filename)

        print(f"[{i}/{len(student_files)}] {filename}")

        wrap_success, _, wrap_error = wrap_code_file(
            str(student_file),
            wrapped_file,
            USE_ENHANCED_WRAPPER
        )

        if not wrap_success:
            results['wrap_failed'] += 1
            results['exec_failed'] += 1
            print(f"    [FAIL] Wrap failed: {wrap_error[:50]}")
            results['details'].append({
                'file': filename,
                'wrap_success': False,
                'exec_success': False,
                'error': f"Wrap failed: {wrap_error}"
            })
            continue

        results['wrap_success'] += 1

        exec_success, exec_stdout, exec_stderr, return_code = run_symbolic_execution(
            wrapped_file,
            MAX_ITER_PER_FILE
        )

        if exec_success:
            results['exec_success'] += 1
            path_count = parse_output(exec_stdout)
            print(f"    [OK] Symbolic execution succeeded - {path_count} paths found")
            results['details'].append({
                'file': filename,
                'wrap_success': True,
                'exec_success': True,
                'path_count': path_count,
                'error': None
            })
        else:
            results['exec_failed'] += 1
            if "timeout" in exec_stderr.lower() or "超时" in exec_stderr:
                results['exec_timeout'] += 1
                print(f"    [TIMEOUT] Symbolic execution timeout")
            else:
                print(f"    [FAIL] Symbolic execution failed")
            results['details'].append({
                'file': filename,
                'wrap_success': True,
                'exec_success': False,
                'path_count': 0,
                'error': exec_stderr[:100] if exec_stderr else "Unknown error"
            })

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("Test complete!")
    print("=" * 70)

    total = results['total']
    print(f"\nTotal: {total} files")
    print(f"Wrap success: {results['wrap_success']}")
    print(f"Wrap failed: {results['wrap_failed']}")
    print(f"Symbolic execution success: {results['exec_success']}")
    print(f"Symbolic execution failed: {results['exec_failed']}")
    print(f"  - Timeout: {results['exec_timeout']}")
    print(f"Total time: {elapsed_time:.2f}s")
    print(f"Average time: {elapsed_time / total:.2f}s/file")

    success_rate = results['exec_success'] / total * 100 if total > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("PyExZ3 Batch Student Code Test Report v2\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Test time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Test directory: {STUDENT_CODE_DIR}\n")
        f.write(f"Wrapper: {'Enhanced' if USE_ENHANCED_WRAPPER else 'Basic'}\n")
        f.write(f"Max iterations: {MAX_ITER_PER_FILE}\n")
        f.write(f"Symbolic execution timeout: {EXEC_TIMEOUT}s\n")
        f.write(f"\nExport config:\n")
        f.write(f"  Enable simplify: {'Yes' if ENABLE_SIMPLIFY else 'No'}\n")
        f.write(f"  Dump constraints: {'Yes' if DUMP_CONSTRAINTS else 'No'}\n")
        f.write(f"  Dump trace: {'Yes' if DUMP_TRACE else 'No'}\n")
        f.write(f"  Dump semantics: {'Yes' if DUMP_SEMANTICS else 'No'}\n")
        f.write(f"  Dump all executions: {'Yes' if DUMP_ALL_EXECUTIONS else 'No'}\n\n")

        f.write("=" * 70 + "\n")
        f.write("Statistics\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total: {total} files\n")
        f.write(f"Wrap success: {results['wrap_success']}\n")
        f.write(f"Wrap failed: {results['wrap_failed']}\n")
        f.write(f"Symbolic execution success: {results['exec_success']}\n")
        f.write(f"Symbolic execution failed: {results['exec_failed']}\n")
        f.write(f"  - Timeout: {results['exec_timeout']}\n")
        f.write(f"Success rate: {success_rate:.1f}%\n")
        f.write(f"Total time: {elapsed_time:.2f}s\n\n")

        f.write("=" * 70 + "\n")
        f.write("Detailed results\n")
        f.write("=" * 70 + "\n")

        for detail in results['details']:
            status = "[OK]" if detail['exec_success'] else "[FAIL]"
            f.write(f"\n{status} {detail['file']}\n")
            if detail['exec_success']:
                f.write(f"    Paths: {detail['path_count']}\n")
            else:
                f.write(f"    Error: {detail['error']}\n")

    print(f"\nReport saved to: {REPORT_FILE}")
    print(f"Wrapped files saved to: {WRAPPED_DIR}")

if __name__ == '__main__':
    main()
