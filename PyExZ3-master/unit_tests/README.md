# PyExZ3 单元测试目录

本目录包含 PyExZ3 项目的单元测试，用于测试各个模块的功能。

## 目录结构

```
unit_tests/
├── README.md          # 本文件
└── test_normalizer.py # 约束规范化模块测试
```

## 运行测试

### 运行所有单元测试
```bash
python -m unittest discover -s unit_tests -p "test_*.py"
```

### 运行特定测试文件
```bash
python unit_tests/test_normalizer.py
```

### 运行特定测试并显示详细信息
```bash
python unit_tests/test_normalizer.py -v
```

## 添加新测试

1. 在 `unit_tests/` 目录下创建新的测试文件，命名为 `test_*.py`
2. 继承 `unittest.TestCase` 类
3. 实现测试方法（以 `test_` 开头）
4. 添加必要的路径设置，确保能够导入 `symbolic` 模块

## 测试分类

### 按模块分类
- `test_normalizer.py`: 约束规范化模块测试

### 按功能分类
- 变量重命名测试
- 表达式标准化测试
- 常量合并测试
- 比较操作规范化测试
