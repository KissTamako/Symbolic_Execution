# PyExZ3 优化版使用指南

## 概述

本文档介绍优化后的 PyExZ3 符号执行工具的使用方法。所有优化都是可选的，默认行为保持不变，确保向后兼容性。

## 优化功能列表

### 1. UNSAT 缓存（默认启用）
- **功能**：缓存已证明为不可满足（UNSAT）的约束组合，避免重复求解
- **实现位置**：`symbolic/z3_wrap.py`
- **默认状态**：✅ 始终启用
- **缓存策略**：LRU（最近最少使用），默认大小限制为 1000 条

### 2. Frontier 约束去重
- **功能**：避免重复处理相同的约束
- **默认状态**：❌ 关闭
- **启用参数**：`--enable-frontier-dedup`

### 3. 搜索策略切换
- **功能**：在广度优先（BFS）和深度优先（DFS）之间切换
- **默认状态**：✅ BFS（广度优先）
- **启用参数**：`--search-strategy=bfs` 或 `--search-strategy=dfs`

### 4. Z3 表达式简化
- **功能**：使用 Z3 内置的 `simplify()` 功能简化约束表达式
- **默认状态**：❌ 关闭
- **启用参数**：`--enable-simplify`

### 5. 前缀去重（简化版）
- **功能**：避免处理具有相同前缀的约束（仅对短路径有效）
- **默认状态**：❌ 关闭
- **启用参数**：`--enable-prefix-dedup`
- **额外参数**：`--max-prefix-length=N`（默认 N=3，只对路径长度 ≤ N 的约束进行前缀检查）

### 6. 增量求解接口
- **功能**：为后续实现真正的增量求解预留接口
- **默认状态**：❌ 关闭
- **启用参数**：`--enable-incremental`

### 7. 导出所有执行的详细信息
- **功能**：为每一次执行生成独立的详细信息文件
- **默认状态**：❌ 关闭
- **启用参数**：`--dump-all-executions`
- **输出目录**：`outputs/<test_name>/executions/`
- **说明**：每个执行都有独立的子目录（`execution_0/`, `execution_1/`, ...），包含完整的 `path.json`、`branch_trace.json`、`semantic_tags.json`

## 使用方法

PyExZ3 支持两种执行模式：**函数执行模式**和**脚本执行模式**。

### 函数执行模式（默认）

**描述**：用于对 Python 文件中的特定函数进行符号执行。

**适用场景**：
- 测试单个函数
- 分析函数在不同输入下的行为
- 探索函数的所有可能执行路径

**基本使用**：

```bash
# 对单个函数进行符号执行（默认使用与文件名同名的函数）
python pyexz3.py test/simple.py

# 指定入口函数
python pyexz3.py --start=my_function test/complex.py

# 对 test 文件夹中的所有测试用例进行测试
python run_tests.py test

# 测试并导出约束、跟踪和语义信息
python run_tests.py test --dump-constraints --dump-trace --dump-semantics
```

### 脚本执行模式

**描述**：用于对整个 Python 脚本进行符号执行，包括其所有语句和函数。

**适用场景**：
- 测试整个脚本
- 分析脚本在不同输入下的行为
- 探索脚本的所有可能执行路径
- 测试包含多个函数和复杂控制流的脚本

**基本使用**：

```bash
# 对单个脚本进行符号执行
python pyexz3.py --mode=script test_script.py

# 对脚本进行符号执行，设置最大迭代次数
python pyexz3.py --mode=script --max-iters=10 test_script_complex.py

# 对脚本进行符号执行并导出信息
python pyexz3.py --mode=script --dump-constraints --dump-trace --dump-semantics test_script.py
```

### 使用优化功能

#### 启用多个优化

**函数模式**：
```bash
# 启用 Frontier 约束去重和 Z3 表达式简化
python pyexz3.py --enable-frontier-dedup --enable-simplify test/simple.py

# 使用 run_tests.py 测试所有用例，启用多个优化
python run_tests.py test --enable-frontier-dedup --enable-simplify
```

**脚本模式**：
```bash
# 启用 Frontier 约束去重和 Z3 表达式简化
python pyexz3.py --mode=script --enable-frontier-dedup --enable-simplify test_script.py
```

#### 切换搜索策略

**函数模式**：
```bash
# 使用 DFS（深度优先）搜索策略
python pyexz3.py --search-strategy=dfs test/simple.py

# 使用 DFS 策略测试所有用例
python run_tests.py test --search-strategy=dfs
```

**脚本模式**：
```bash
# 使用 DFS（深度优先）搜索策略
python pyexz3.py --mode=script --search-strategy=dfs test_script.py
```

#### 启用前缀去重

**函数模式**：
```bash
# 启用前缀去重，使用默认最大前缀长度 3
python pyexz3.py --enable-prefix-dedup test/simple.py

# 启用前缀去重，自定义最大前缀长度为 5
python pyexz3.py --enable-prefix-dedup --max-prefix-length=5 test/simple.py

# 使用前缀去重测试所有用例
python run_tests.py test --enable-prefix-dedup --max-prefix-length=5
```

**脚本模式**：
```bash
# 启用前缀去重，使用默认最大前缀长度 3
python pyexz3.py --mode=script --enable-prefix-dedup test_script.py

# 启用前缀去重，自定义最大前缀长度为 5
python pyexz3.py --mode=script --enable-prefix-dedup --max-prefix-length=5 test_script.py
```

#### 组合使用多个优化

**函数模式**：
```bash
# 组合使用多个优化进行符号执行
python pyexz3.py \
  --enable-frontier-dedup \
  --search-strategy=dfs \
  --enable-simplify \
  --enable-prefix-dedup \
  --max-prefix-length=4 \
  test/simple.py

# 组合使用多个优化测试所有用例
python run_tests.py test \
  --enable-frontier-dedup \
  --search-strategy=dfs \
  --enable-simplify \
  --enable-prefix-dedup \
  --max-prefix-length=4 \
  --dump-constraints \
  --dump-trace \
  --dump-semantics
```

**脚本模式**：
```bash
# 组合使用多个优化进行脚本符号执行
python pyexz3.py --mode=script \
  --enable-frontier-dedup \
  --search-strategy=dfs \
  --enable-simplify \
  --enable-prefix-dedup \
  --max-prefix-length=4 \
  test_script.py
```

## 完整参数列表

### pyexz3.py 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-l, --log` | 保存日志输出到文件 | - |
| `-s, --start` | 指定入口点 | - |
| `-g, --graph` | 生成执行树的 DOT 图 | False |
| `-m, --max-iters` | 运行指定次数的迭代 | 0 |
| `--cvc` | 使用 CVC SMT 求解器 | False |
| `--z3` | 使用 Z3 SMT 求解器（默认） | True |
| `--mode` | 执行模式：function\|script | function |
| `--dump-constraints` | 导出约束到文件 | False |
| `--dump-trace` | 导出执行跟踪到文件 | False |
| `--dump-semantics` | 导出语义信息到文件 | False |
| `--enable-unsat-cache` | 启用 UNSAT 缓存优化 | True（始终启用） |
| `--enable-frontier-dedup` | 启用 Frontier 约束去重 | False |
| `--search-strategy` | 搜索策略：bfs\|dfs | bfs |
| `--enable-simplify` | 启用 Z3 表达式简化 | False |
| `--enable-prefix-dedup` | 启用前缀去重（简化版） | False |
| `--max-prefix-length` | 前缀去重的最大路径长度 | 3 |
| `--enable-incremental` | 启用增量求解接口 | False |
| `--dump-all-executions` | 导出所有执行的详细信息 | False |

### run_tests.py 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--cvc` | 使用 CVC SMT 求解器 | False |
| `--z3` | 使用 Z3 SMT 求解器（默认） | True |
| `--dump-constraints` | 导出约束到文件 | False |
| `--dump-trace` | 导出执行跟踪到文件 | False |
| `--dump-semantics` | 导出语义信息到文件 | False |
| `--enable-unsat-cache` | 启用 UNSAT 缓存优化 | True（始终启用） |
| `--enable-frontier-dedup` | 启用 Frontier 约束去重 | False |
| `--search-strategy` | 搜索策略：bfs\|dfs | bfs |
| `--enable-simplify` | 启用 Z3 表达式简化 | False |
| `--enable-prefix-dedup` | 启用前缀去重（简化版） | False |
| `--max-prefix-length` | 前缀去重的最大路径长度 | 3 |
| `--enable-incremental` | 启用增量求解接口 | False |
| `--dump-all-executions` | 导出所有执行的详细信息 | False |

## 优化建议

### 小型程序（路径较少）
- 使用默认配置即可
- 如果遇到重复约束，考虑启用 `--enable-frontier-dedup`

### 中型程序（路径中等）
- 建议启用 `--enable-simplify` 来简化约束
- 可以尝试切换搜索策略 `--search-strategy=dfs`
- 如果发现重复的前缀路径，启用 `--enable-prefix-dedup`

### 大型程序（路径较多）
- 组合使用多个优化
- 启用 `--enable-frontier-dedup` 和 `--enable-prefix-dedup`
- 根据程序特点选择合适的搜索策略
- 启用 `--enable-simplify` 来减少约束复杂度

## 输出文件

启用 `--dump-constraints`、`--dump-trace`、`--dump-semantics` 后，输出文件将保存在 `outputs/<test_name>/` 目录下：

- `path_<timestamp>.json` - 路径信息
- `branch_trace_<timestamp>.json` - 分支跟踪
- `semantic_tags_<timestamp>.json` - 语义标签
- `frontier_<timestamp>.json` - Frontier 约束
- `execution_summary_<timestamp>.json` - 执行摘要
- `execution_summary_<timestamp>.smt2` - SMT 格式的执行摘要

## 示例

### 示例 1：基本测试
```bash
python run_tests.py test
```

### 示例 2：完整导出
```bash
python run_tests.py test --dump-constraints --dump-trace --dump-semantics
```

### 示例 3：使用优化（推荐配置）
```bash
python run_tests.py test --enable-simplify --dump-constraints --dump-trace --dump-semantics
```

### 示例 4：尝试更多优化（谨慎使用）
```bash
# 注意：DFS和前缀去重可能对某些程序有问题，请先在小型程序上测试
python run_tests.py test \
  --enable-frontier-dedup \
  --enable-simplify \
  --enable-prefix-dedup \
  --max-prefix-length=2
```

### 示例 5：单个文件优化执行（推荐配置）
```bash
python pyexz3.py --enable-simplify --dump-constraints --dump-trace --dump-semantics test/simple.py
```

## 注意事项

1. **向后兼容性**：所有优化都是可选的，默认行为与原始 PyExZ3 完全一致
2. **小步快走**：建议逐步启用优化，先测试单个优化的效果，再组合使用
3. **性能权衡**：某些优化可能会增加预处理时间，但减少求解时间
4. **内存使用**：UNSAT 缓存和前缀去重会占用额外内存，对于超大型程序需要注意
5. **充分测试**：启用新优化后，建议先在小型测试用例上验证效果
6. **DFS 搜索策略** ： --search-strategy=dfs 可能导致某些递归程序（如 gcd.py ）失败，建议优先使用默认的 BFS 策略
- **前缀去重** ： --enable-prefix-dedup 功能比较激进，可能会去掉一些合法路径，建议谨慎使用
- **逐步验证** ：建议先测试单个优化的效果，确认无误后再组合使用
- **frontier** 为空是正常的 ：当所有路径都被探索完时，frontier_summary.json 为空是正常的
- **--dump-all-executions 存储空间**：启用后会为每次执行生成独立的文件，对于有大量路径的程序会占用较多存储空间，建议谨慎使用

## 技术细节

### UNSAT 缓存
- 使用 `OrderedDict` 实现 LRU 策略
- 默认缓存大小：1000 条约束
- 通过 `getStats()` 获取统计信息（总调用数、缓存命中数、缓存未命中数）

### Frontier 约束去重
- 使用约束对象的 id 作为简单哈希
- 仅在添加到队列时检查
- 避免重复处理相同的约束对象

### 前缀去重
- 只对路径长度 ≤ `max_prefix_length` 的约束进行检查
- 使用谓词表达式的字符串表示生成前缀键
- 避免过度去重，保持探索完整性

### Z3 表达式简化
- 在添加约束到求解器前调用 Z3 的 `simplify()`
- 可以减少约束复杂度，加快求解速度

### Concolic执行模式
- 结合具体执行和符号执行的优点，提高执行效率
- 首先生成具体值并执行，然后基于执行结果生成符号约束
- 支持多种具体值生成策略：random、guided、hybrid

### 智能路径探索策略
- 基于路径长度和覆盖率的智能路径选择
- 计算路径优先级，优先选择较短路径和覆盖新代码的路径
- 支持动态权重调整，根据执行进度调整各维度的权重

### 路径剪枝
- 通过语义相似性、执行成本和循环检测等方式剪枝无效或冗余路径
- 避免重复探索语义相似的路径
- 剪枝执行成本过高的路径
- 检测并剪枝包含循环的路径

### 混合搜索策略
- 在执行过程中自动切换搜索策略
- 结合不同策略的优点，提高路径覆盖能力
- 默认在第5次迭代后切换搜索策略
