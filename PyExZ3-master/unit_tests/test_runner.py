import sys
import os
import traceback

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sys.tracebacklimit = 100

try:
    import pyexz3
    # 直接运行pyexz3模块
    sys.argv = ['pyexz3.py', 'test/simple.py']
    pyexz3.main()
except Exception as e:
    traceback.print_exc()
