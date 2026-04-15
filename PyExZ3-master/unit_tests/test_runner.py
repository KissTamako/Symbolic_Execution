import sys
import traceback

sys.tracebacklimit = 100

try:
    import pyexz3
    # 直接运行pyexz3模块
    sys.argv = ['pyexz3.py', 'test/simple.py']
    pyexz3.main()
except Exception as e:
    traceback.print_exc()
