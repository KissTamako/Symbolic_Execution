# Copyright: see copyright.txt
"""
AST转换器：常量提升（Constant Upcasting）技术实现
将常量方法调用转换为符号对象方法调用，防止符号信息丢失

转换示例：
- "abc".contains(x) → SymbolicStr("const", "abc", "abc").contains(x)
- 5.__add__(x) → SymbolicInteger("const", 5, 5).__add__(x)
- 3.14.__add__(x) → SymbolicFloat("const", 3.14, 3.14).__add__(x)
"""

import ast
import sys

class ConstantUpcaster(ast.NodeTransformer):
    """
    AST转换器：将常量提升为符号对象
    
    核心思想：
    1. 识别常量方法调用模式：constant.method(args)
    2. 将常量转换为对应的符号对象构造函数
    3. 保持方法调用和参数不变
    """
    
    def __init__(self):
        # 内置构造函数名称到符号类的映射
        self.builtin_constructors = {
            'int': 'SymbolicInteger',
            'str': 'SymbolicStr',
            'range': 'SymbolicRange',
            'float': 'SymbolicFloat',
            'bool': 'SymbolicInteger',  # bool暂时使用SymbolicInteger
            'list': 'SymbolicList',
            'dict': 'SymbolicDict',
        }
    
    def visit_Call(self, node):
        # 先递归处理子节点
        node = self.generic_visit(node)
        
        # 检查是否是常量方法调用
        if isinstance(node.func, ast.Attribute):
            if self._is_constant(node.func.value):
                # 将常量转换为符号对象构造函数调用
                return self._convert_constant_call(node)
        
        # 检查是否是内置构造函数调用
        if self._is_builtin_constructor(node):
            # 将内置构造函数转换为符号构造函数调用
            return self._convert_builtin_constructor_call(node)
        
        return node
    
    def _is_constant(self, node):
        """判断节点是否是常量"""
        return isinstance(node, ast.Constant)
    
    def _convert_constant_call(self, call_node):
        """将常量方法调用转换为符号对象方法调用"""
        const_node = call_node.func.value
        attr_name = call_node.func.attr
        
        # 根据常量类型选择符号类
        const_value = const_node.value
        
        # 确定符号类名称
        if isinstance(const_value, str):
            sym_class = "SymbolicStr"
        elif isinstance(const_value, int):
            sym_class = "SymbolicInteger"
        elif isinstance(const_value, float):
            sym_class = "SymbolicFloat"
        elif isinstance(const_value, bool):
            # Python的bool是int的子类，但我们需要单独处理
            sym_class = "SymbolicInteger"  # 暂时使用SymbolicInteger，可以创建SymbolicBool
        elif const_value is None:
            # None不转换
            return call_node
        else:
            # 其他类型（bytes, ellipsis等）暂不转换
            return call_node
        
        # 创建 SymbolicClass("const", value, value).method(args) 的AST
        # 1. 创建 SymbolicClass 构造函数调用
        sym_call = self._create_symbolic_constructor(sym_class, const_value)
        
        # 2. 创建属性访问
        new_attr = ast.Attribute(value=sym_call, attr=attr_name, ctx=ast.Load())
        
        # 3. 创建新的调用节点
        new_call = ast.Call(
            func=new_attr,
            args=call_node.args,
            keywords=call_node.keywords
        )
        
        # 复制位置信息
        ast.copy_location(new_call, call_node)
        
        return new_call
    
    def _create_symbolic_constructor(self, class_name, value):
        """创建符号对象构造函数调用AST"""
        # 创建参数：name="const", concrete_value=value, symbolic_expr=value
        const_str = ast.Constant(value="const")
        value_node = ast.Constant(value=value)
        
        # 创建类名节点
        sym_class = ast.Name(id=class_name, ctx=ast.Load())
        
        # 创建调用节点：SymbolicClass("const", value, value)
        call = ast.Call(
            func=sym_class,
            args=[const_str, value_node, value_node],
            keywords=[]
        )
        
        return call
    
    def _create_ast_constant(self, value):
        """创建AST常量节点（兼容性封装）"""
        return ast.Constant(value=value)
    
    def _is_builtin_constructor(self, call_node):
        """判断是否是内置构造函数调用"""
        if not isinstance(call_node.func, ast.Name):
            return False
        
        func_name = call_node.func.id
        return func_name in self.builtin_constructors
    
    def _convert_builtin_constructor_call(self, call_node):
        """将内置构造函数转换为符号构造函数调用"""
        func_name = call_node.func.id
        sym_class = self.builtin_constructors[func_name]
        
        # 创建 SymbolicClass.from_symbolic(args) 的AST
        # 1. 创建 SymbolicClass 类名节点
        sym_class_node = ast.Name(id=sym_class, ctx=ast.Load())
        
        # 2. 创建属性访问：SymbolicClass.from_symbolic
        attr_node = ast.Attribute(value=sym_class_node, attr='from_symbolic', ctx=ast.Load())
        
        # 3. 创建新的调用节点：SymbolicClass.from_symbolic(args)
        new_call = ast.Call(
            func=attr_node,
            args=call_node.args,
            keywords=call_node.keywords
        )
        
        # 复制位置信息
        ast.copy_location(new_call, call_node)
        
        return new_call


def transform_source_code(source_code, enable_upcasting=True):
    """
    转换源代码，将常量提升为符号对象
    
    参数：
    source_code: 原始源代码字符串
    enable_upcasting: 是否启用常量提升
    
    返回：
    transformed_source: 转换后的源代码字符串（用于调试）
    code_obj: 编译后的代码对象（用于执行）
    """
    if not enable_upcasting:
        # 不启用转换时直接编译
        return source_code, compile(source_code, '<original>', 'exec')
    
    try:
        # 解析AST
        tree = ast.parse(source_code)
        
        # 应用转换
        transformer = ConstantUpcaster()
        transformed_tree = transformer.visit(tree)
        
        # 固定AST（确保所有节点都有正确的父节点引用）
        ast.fix_missing_locations(transformed_tree)
        
        # 编译转换后的AST
        code_obj = compile(transformed_tree, '<transformed>', 'exec')
        
        # 将AST转换回源代码（用于调试，Python 3.9+支持）
        transformed_source = ""
        if hasattr(ast, 'unparse'):
            try:
                transformed_source = ast.unparse(transformed_tree)
            except Exception:
                # unparse可能失败，这不是关键功能
                transformed_source = "<无法反解析AST>"
        
        return transformed_source, code_obj
        
    except Exception as e:
        print(f"[AST转换警告] 转换失败，使用原始代码: {e}")
        # 失败时返回原始代码
        import traceback
        traceback.print_exc()
        return source_code, compile(source_code, '<original>', 'exec')


def test_ast_transformation():
    """测试AST转换功能"""
    test_cases = [
        # (原始代码, 期望转换)
        ('"abc".__contains__("b")', 
         'SymbolicStr("const", "abc", "abc").__contains__("b")'),
        
        ('(5).__add__(3)', 
         'SymbolicInteger("const", 5, 5).__add__(3)'),
        
        ('3.14.__add__(1.0)', 
         'SymbolicFloat("const", 3.14, 3.14).__add__(1.0)'),
        
        # 复杂表达式
        ('x = "hello".upper() + " world"', 
         'x = SymbolicStr("const", "hello", "hello").upper() + " world"'),
        
        # 嵌套调用
        ('"abc".find("b") + 5', 
         'SymbolicStr("const", "abc", "abc").find("b") + 5'),
    ]
    
    print("测试AST转换:")
    for i, (original, expected_snippet) in enumerate(test_cases):
        transformed_source, _ = transform_source_code(original)
        print(f"测试 {i+1}:")
        print(f"  原始: {original}")
        print(f"  转换: {transformed_source[:100] if transformed_source else '<无输出>'}") 
        print(f"  期望包含: {expected_snippet}")
        print()


if __name__ == "__main__":
    # 直接运行此文件进行测试
    test_ast_transformation()
    print("AST转换器模块加载成功")