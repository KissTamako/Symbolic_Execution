# Copyright: see copyright.txt
"""
路径管理工具，解决PyExZ3项目中的导入和路径问题。

主要功能：
1. 自动设置项目路径确保正确导入
2. 提供路径调试信息
3. 导入错误诊断
"""

import sys
import os
import traceback

def find_project_root(start_path=None):
    """
    搜索PyExZ3项目根目录
    
    参数:
        start_path (str): 开始搜索的路径，如果为None则使用当前文件所在目录
    
    返回:
        str: 项目根目录路径，如果找不到则返回None
    """
    if start_path is None:
        start_path = os.path.dirname(os.path.abspath(__file__))
    
    current = os.path.abspath(start_path)
    
    # 查找包含pyexz3.py的目录
    while True:
        # 检查当前目录是否有pyexz3.py或symbolic目录
        pyexz3_file = os.path.join(current, 'pyexz3.py')
        symbolic_dir = os.path.join(current, 'symbolic')
        
        if os.path.exists(pyexz3_file) or os.path.exists(symbolic_dir):
            return current
        
        # 到达根目录，停止搜索
        parent = os.path.dirname(current)
        if parent == current:
            break
        
        current = parent
    
    # 如果找不到，尝试查找包含'symbolic'目录的上级目录
    current = os.path.abspath(start_path)
    while True:
        for item in os.listdir(current):
            if item == 'symbolic' and os.path.isdir(os.path.join(current, item)):
                # 检查该目录是否是PyExZ3项目
                test_path = os.path.join(current, item)
                if os.path.exists(os.path.join(test_path, '__init__.py')):
                    return current
        
        parent = os.path.dirname(current)
        if parent == current:
            break
        
        current = parent
    
    return None

def setup_project_paths(start_path=None):
    """
    设置项目路径确保正确导入
    
    参数:
        start_path (str): 项目根目录路径，如果为None则自动查找
    
    返回:
        tuple: (project_root, symbolic_dir)
    """
    # 查找项目根目录
    if start_path is None:
        project_root = find_project_root()
    else:
        project_root = start_path
    
    if project_root is None:
        # 如果找不到项目根目录，使用传统方法
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        print(f"[WARN] Could not find project root, using: {project_root}")
    
    # 确保project_root存在
    if not os.path.exists(project_root):
        print(f"[ERROR] Project root does not exist: {project_root}")
        # 尝试使用当前工作目录
        project_root = os.getcwd()
    
    symbolic_dir = os.path.join(project_root, 'symbolic')
    
    # 如果symbolic目录不存在，尝试在当前文件所在目录查找
    if not os.path.exists(symbolic_dir):
        # 尝试使用当前文件所在目录作为symbolic目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(current_dir) == 'symbolic' and os.path.exists(os.path.join(current_dir, '__init__.py')):
            symbolic_dir = current_dir
            project_root = os.path.dirname(current_dir)
        else:
            print(f"[WARN] Symbolic directory not found at: {symbolic_dir}")
    
    # 添加项目根目录到sys.path（如果尚未存在）
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # 添加symbolic目录到sys.path（如果尚未存在）
    if symbolic_dir not in sys.path:
        sys.path.insert(0, symbolic_dir)
    
    return project_root, symbolic_dir

def debug_path_info():
    """
    打印路径调试信息，用于诊断导入问题
    """
    print("=== PyExZ3 路径调试信息 ===")
    print(f"Python解释器: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 获取symbolic目录路径
    symbolic_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Symbolic目录: {symbolic_dir}")
    
    project_root = os.path.dirname(symbolic_dir)
    print(f"项目根目录: {project_root}")
    
    print("sys.path内容 (前10项):")
    for i, path in enumerate(sys.path[:10]):
        exists = os.path.exists(path)
        marker = "✓" if exists else "✗"
        print(f"  [{i}] {marker} {path}")
    
    if len(sys.path) > 10:
        print(f"  ... 还有 {len(sys.path) - 10} 项")

def diagnose_import_error(module_name, error):
    """
    分析导入错误并提供解决方案
    
    参数:
        module_name (str): 导入失败的模块名
        error (Exception): 导入错误异常
    
    返回:
        list: 建议的解决方案列表
    """
    suggestions = []
    
    error_str = str(error)
    
    # 检查常见错误模式
    if "No module named" in error_str:
        missing_module = error_str.split("'")[1] if "'" in error_str else module_name
        suggestions.append(f"找不到模块: '{missing_module}'")
        suggestions.append(f"当前sys.path: {sys.path}")
        
        # 检查是否缺少symbolic目录
        symbolic_dir = os.path.dirname(os.path.abspath(__file__))
        if symbolic_dir not in sys.path:
            suggestions.append(f"需要添加symbolic目录到sys.path: {symbolic_dir}")
        
        # 检查项目结构
        project_root = os.path.dirname(symbolic_dir)
        if not os.path.exists(os.path.join(project_root, "symbolic")):
            suggestions.append(f"项目结构可能不正确，缺少symbolic目录")
    
    elif "cannot import name" in error_str:
        import_name = error_str.split("'")[1] if "'" in error_str else ""
        suggestions.append(f"导入名称错误: '{import_name}'")
        suggestions.append("检查目标模块中是否存在该名称")
    
    elif "attempted relative import" in error_str and "no known parent package" in error_str:
        suggestions.append("相对导入错误: 当前模块不是包的一部分")
        suggestions.append("尝试使用绝对导入或确保模块在正确的包结构中")
    
    # 通用建议
    suggestions.append("尝试运行: python -c \"import sys; sys.path.insert(0, 'PyExZ3-master'); from symbolic.loader import *\"")
    suggestions.append("确保从项目根目录运行: cd PyExZ3-master && python pyexz3.py ...")
    
    return suggestions

def ensure_paths_for_file(file_path):
    """
    确保给定文件的路径在sys.path中，用于动态导入
    
    参数:
        file_path (str): 要导入的文件路径
    
    返回:
        str: 导入时使用的模块名
    """
    file_dir = os.path.dirname(os.path.abspath(file_path))
    
    # 添加文件所在目录到sys.path（如果尚未存在）
    if file_dir not in sys.path:
        sys.path.insert(0, file_dir)
    
    # 返回模块名（去掉.py扩展名）
    module_name = os.path.basename(file_path)
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    
    return module_name

def setup_global_paths():
    """
    全局路径设置，应在所有模块导入前调用
    
    返回:
        dict: 包含设置的路径信息
    """
    # 确保设置了项目路径
    project_root, symbolic_dir = setup_project_paths()
    
    # 打印调试信息（仅在需要时）
    debug_mode = os.environ.get('PYEXZ3_DEBUG_PATHS', '0') == '1'
    if debug_mode:
        debug_path_info()
    
    return {
        'project_root': project_root,
        'symbolic_dir': symbolic_dir,
        'python_path': sys.executable,
        'working_dir': os.getcwd()
    }

def safe_import_module(file_path, module_name=None):
    """
    安全地导入模块，自动处理路径问题
    
    参数:
        file_path (str): Python文件路径
        module_name (str, optional): 模块名，如果为None则从文件名推导
    
    返回:
        module: 导入的模块对象
    
    异常:
        ImportError: 导入失败时抛出
    """
    import importlib.util
    
    # 确保路径
    if module_name is None:
        module_name = ensure_paths_for_file(file_path)
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"Could not create spec for {file_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        # 提供更详细的错误信息
        error_msg = f"Failed to import {file_path}: {e}"
        # 检查常见问题
        if not os.path.exists(file_path):
            error_msg += f"\nFile does not exist: {file_path}"
        elif not os.path.isfile(file_path):
            error_msg += f"\nPath is not a file: {file_path}"
        elif not file_path.endswith('.py'):
            error_msg += f"\nFile is not a Python file: {file_path}"
        
        raise ImportError(error_msg)

def setup_paths_for_dynamic_import(file_path):
    """
    为动态导入设置路径，返回模块名
    
    参数:
        file_path (str): Python文件路径
    
    返回:
        str: 模块名
    """
    return ensure_paths_for_file(file_path)

def import_with_fallback(file_path, module_name=None):
    """
    导入模块，提供回退机制
    
    参数:
        file_path (str): Python文件路径
        module_name (str, optional): 模块名
    
    返回:
        tuple: (module, used_fallback)
    """
    try:
        # 首先尝试safe_import_module
        module = safe_import_module(file_path, module_name)
        return module, False
    except ImportError as e:
        print(f"[WARN] safe_import_module failed: {e}")
        print(f"[WARN] Falling back to traditional import...")
        
        # 回退到传统导入
        if module_name is None:
            module_name = os.path.basename(file_path)
            if module_name.endswith('.py'):
                module_name = module_name[:-3]
        
        # 确保路径在sys.path中
        file_dir = os.path.dirname(os.path.abspath(file_path))
        if file_dir not in sys.path:
            sys.path.insert(0, file_dir)
        
        try:
            module = __import__(module_name)
            return module, True
        except ImportError as e2:
            raise ImportError(f"Both import methods failed:\n1. {e}\n2. {e2}")

# 自动设置路径（当模块被导入时）
_ = setup_project_paths()
