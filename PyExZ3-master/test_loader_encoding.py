#!/usr/bin/env python3
"""测试loader编码问题"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# 创建测试文件
test_code = '''def test_func():
    return "hello"
'''

# 写入临时文件
import tempfile
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(test_code)
    temp_file = f.name

print(f"临时文件: {temp_file}")
print(f"文件存在: {os.path.exists(temp_file)}")

# 尝试读取文件
try:
    with open(temp_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print("utf-8读取成功")
    print(f"内容: {content}")
except Exception as e:
    print(f"utf-8读取失败: {e}")

# 尝试其他编码
try:
    with open(temp_file, 'r', encoding='gbk') as f:
        content = f.read()
    print("gbk读取成功")
except Exception as e:
    print(f"gbk读取失败: {e}")

# 尝试二进制读取
try:
    with open(temp_file, 'rb') as f:
        binary = f.read()
    print(f"二进制读取成功，长度: {len(binary)}")
    print(f"前100字节: {binary[:100]}")
except Exception as e:
    print(f"二进制读取失败: {e}")

# 清理
import os
if os.path.exists(temp_file):
    os.unlink(temp_file)
    print(f"清理临时文件")

print("\n测试系统的默认编码:")
print(f"sys.getdefaultencoding(): {sys.getdefaultencoding()}")
import locale
print(f"locale.getpreferredencoding(): {locale.getpreferredencoding()}")
