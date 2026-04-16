# PyExZ3 修改与检测报告

## 1. 本次目标

本次修改主要针对前面已经定位出的几个关键问题：

1. AST 转换不完整，导致 `elif`/嵌套分支位置采集错误，`int/str/float/range/input` 包装不一致。
2. `path.smt2` 导出的并不是“当前执行路径约束”，而是“前沿约束求解文件”。
3. SMT 变量抽取会把辅助变量 `se` 混进约束文件。
4. Windows 路径字符串在 AST 注入时被错误转义，出现 `\u0007` 一类污染。
5. `count_input_calls()` 用正则统计 `input()`，会把注释中的 `input()` 也算进去。
6. `test_optimization_effect.py` 使用裸 `python` 且不汇总失败，存在假通过。
7. `Replay mismatch` 调试输出过于嘈杂。

## 2. 实际修改文件

本次改动涉及以下文件：

- `symbolic/ast_transform.py`
- `symbolic/runtime_helpers.py`
- `symbolic/loader.py`
- `symbolic/script_runner.py`
- `symbolic/exporters/smt_exporter.py`
- `symbolic/explore.py`
- `symbolic/path_to_constraint.py`
- `symbolic/symbolic_types/symbolic_type.py`
- `symbolic/predicate.py`
- `pyexz3.py`
- `test_optimization_effect.py`

## 3. 修改内容

### 3.1 AST 转换层

文件：`symbolic/ast_transform.py`

修改点：

- 改为直接使用 `ast` 节点构造，不再用 `parse('_se_input()')` 或字符串拼 AST。
- `visit_Call()` 统一包装以下内建调用：
  - `input -> _se_input`
  - `int -> _se_int`
  - `str -> _se_str`
  - `float -> _se_float`
  - `range -> _se_range`
- `visit_If()`、`visit_While()` 先 `generic_visit()` 再包裹条件，修复嵌套 `if/elif/while` 未递归插桩的问题。
- `_se_branch_hook(...)` 直接作为 AST 调用注入，并把文件名预先规范化为 `/` 风格路径。

效果：

- `elif` 分支现在能被正确插桩。
- Windows 路径不再因为字符串转义出错。

### 3.2 运行时 helper

文件：`symbolic/runtime_helpers.py`

修改点：

- `_se_int/_se_str/_se_float` 改为支持 `*args, **kwargs`。
- 对符号对象优先调用其 `__int2__/__str2__/__float2__`，避免简单强转后丢失符号表达式。
- `_branch_hook()` 中对文件路径再做一次规范化。

效果：

- 避免了 `int(symbolic)` 等操作把符号信息退化成辅助名 `se`。
- 后续 SMT 导出不再出现 `declare-const se Int`。

### 3.3 function/script 执行环境

文件：

- `symbolic/loader.py`
- `symbolic/script_runner.py`

修改点：

- 在 AST 执行前注入：
  - `_se_branch_hook`
  - `_se_input`
  - `_se_int`
  - `_se_str`
  - `_se_float`
  - `_se_range`
- `script_runner.py` 不再把 `_se_int/_se_str/_se_float` 直接绑定到符号类本身，而是绑定到运行时 helper。
- script 执行时补充 `__file__`、当前文件路径上下文。

效果：

- function mode 与 script mode 的包装行为一致。
- `input()`、`int()` 等包装函数现在在两个模式下都能真实生效。

### 3.4 SMT 导出语义修正

文件：

- `symbolic/exporters/smt_exporter.py`
- `symbolic/explore.py`

修改点：

- 重写 SMT 导出器，拆分“当前执行路径导出”和“前沿约束导出”两种语义。
- `export_executed_path()` 直接把当前路径上每个谓词按实际分支结果写入 SMT。
- `export_frontier()` 继续导出前沿求解文件，语义仍是 `asserts + not(query)`。
- 变量提取改为遍历真实符号表达式树，并根据类型推断 `Int/Real/String/Bool`。
- 忽略辅助名字 `se`、`const`。
- `_export_results()` 始终把当前执行路径导出到 `path.smt2`，前沿约束单独放在 `frontier/`。

效果：

- `path.smt2` 终于表示“当前执行路径约束”，不再混入 `not(query)`。
- 变量声明不再错误包含 `se`。

### 3.5 路径回放与位置字段兼容

文件：

- `symbolic/path_to_constraint.py`
- `symbolic/symbolic_types/symbolic_type.py`
- `symbolic/predicate.py`

修改点：

- `Replay mismatch` 改为只在符号表达式匹配但方向异常时输出 debug 日志，不再刷屏。
- 回退分支位置采集时，不再把函数名误写入列号字段。
- `Predicate` 增加 `source_col` 兼容字段，兼容现有 JSON 导出逻辑。

效果：

- `source_col` 不再出现 `"andor"`、`"whileloop"` 这类函数名污染。
- `source_spans` 列号恢复正常。

### 3.6 CLI 与测试脚本

文件：

- `pyexz3.py`
- `test_optimization_effect.py`

修改点：

- `count_input_calls()` 改为 AST 统计真实 `input()` 调用。
- script mode 结果判定改为：所有执行返回值都为 `None` 才视为成功。
- `test_optimization_effect.py` 改为使用 `sys.executable`。
- `test_optimization_effect.py` 现在会汇总子用例失败并返回非 0。

效果：

- `test_input.py` 中注释里的 `input()` 不再被误计数。
- 优化测试脚本不再“假通过”。

## 4. 验证结果

### 4.1 语法检查

命令：

```powershell
python -m py_compile pyexz3.py symbolic/ast_transform.py symbolic/runtime_helpers.py symbolic/loader.py symbolic/script_runner.py symbolic/exporters/smt_exporter.py symbolic/explore.py symbolic/path_to_constraint.py symbolic/symbolic_types/symbolic_type.py test_optimization_effect.py
```

结果：

- 通过。

### 4.2 单元测试

命令：

```powershell
python -m unittest discover -s unit_tests -p "test_*.py" -v
```

结果：

- 12/12 通过。

### 4.3 主测试集

命令：

```powershell
python run_tests.py test
```

结果：

- 大部分测试通过。
- 仍失败：`fp.py`

结论：

- 本次改动没有破坏原有整数/分支主流程。
- 当前仓库仍存在浮点支持不足的问题，这不是本轮修改新引入的主问题，而是原有能力边界仍未补齐。

### 4.4 定向验证 1：当前路径 SMT 是否正确

命令：

```powershell
python pyexz3.py --dump-constraints test/abs_test.py
```

检查文件：`outputs/abs_test/path.smt2`

实际结果：

```smt2
(declare-const a Int)
(declare-const b Int)

; ((< a 0)) (True)
(assert (< a 0))
; ((== (abs a) b)) (True)
(assert (= (abs a) b))
```

结论：

- 正确。
- 这已经是当前执行路径本身。
- 不再错误写成 `(assert (not (= (abs a) b)))`。
- 不再出现 `declare-const se Int`。

### 4.5 定向验证 2：源码位置信息是否正确

命令：

```powershell
python pyexz3.py --dump-constraints test/source_location_test.py
```

检查文件：`outputs/source_location_test/path.json`

关键结果：

- 第一条分支：`source_line = 5`
- 第二条分支：`source_line = 7`
- `source_col = [4, 4]`

结论：

- `elif x < 0` 已恢复到正确的第 7 行。
- 列号字段恢复正常。
- 文件路径为规范化后的绝对路径，不再出现转义污染。

### 4.6 定向验证 3：`input()` 统计是否修正

命令：

```powershell
python pyexz3.py --mode script --dump-constraints test_input.py
```

关键结果：

- 输出：`Found 2 input() call(s)`

结论：

- 之前注释中的 `input()` 被误计数为第 3 个输入。
- 现在已修正为真实的 2 个调用点。

### 4.7 定向验证 4：优化测试脚本是否还会假通过

命令：

```powershell
python test_optimization_effect.py
```

结果：

- 现在脚本会真实返回失败。
- 暴露出：
  - `simple.py` 在 `concrete` 模式下无法覆盖完整 expected set。
  - `binary_search.py` 在 `concolic/concrete` 模式下仍无法满足 expected set。

结论：

- 这是正确行为。
- 之前该脚本会因为子进程调用方式和失败汇总缺失而出现“假绿”。
- 本次修改后，测试脚本本身的可信度已经恢复。

## 5. 最终结论

### 5.1 本轮修复成功的内容

- 当前执行路径约束导出已修正。
- `se` 辅助变量泄漏已修正。
- `elif`/嵌套分支位置信息已修正。
- Windows 路径字符串污染已修正。
- `input()` 调用计数已修正。
- 优化效果脚本的假通过问题已修正。

### 5.2 当前仍未完全解决的问题

1. `fp.py` 仍失败。
   - 根因是浮点相关符号表达式/求解支持不完整。

2. `concrete` / `concolic` 模式覆盖率仍不足。
   - 本轮修的是“测试脚本是否诚实报告”，不是“这两种模式本身是否足够强”。

3. script mode 的输入建模仍偏弱。
   - 目前 `input()` 仍默认建模为整数输入序列。
   - 对字符串脚本、`list(input())`、`eval(input())` 这类学生程序仍不够鲁棒。

4. loader 在部分上下文下仍会先尝试错误路径，再 fallback 导入。
   - 现象是个别测试会打印 `Couldn't import simple` 之类噪声。
   - 功能不受阻，但实现还不够干净。

## 6. 后续建议

建议下一步按优先级推进：

1. 补 `input` 输入模型。
   - 支持 `str/int/float` 多类型输入。
   - 为脚本模式增加显式输入 schema 或延迟按需生成输入。

2. 补浮点路径支持。
   - 先把 `fp.py` 跑通，再考虑更复杂 real/float 约束。

3. 强化 concolic 策略。
   - 当前 `concrete`/`concolic` 只做了基础框架，覆盖能力还明显不够。

4. 结构化导出语义特征。
   - 在当前已经正确的 `path.json/path.smt2` 基础上，继续抽取：
     - 路径谓词序列
     - 归一化约束模板
     - 分支位置序列
     - 变量参与图
     - 路径摘要向量
   - 这一步完成后，再去做类似 PaCon 的策略聚类会更稳。

## 7. 结论性评价

1. 还不能通过所有测试用例。
2. 约束信息“部分正确”。
3. 更准确地说：整数/分支类程序的原始路径约束已经基本正确，但浮点路径和归一化后的约束特征还不完全正确。

**主要发现**
- 高：`run_tests.py test` 仍然失败，失败用例是 `fp.py`。
  原因不是这轮 `path.smt2` 修改，而是浮点求解链路本身没做完。
  相关位置：
  [z3_wrap.py](Symbolic_Execution-main/PyExZ3-master/symbolic/z3_wrap.py#L142)
  [float.py](Symbolic_Execution-main/PyExZ3-master/symbolic/z3_expr/float.py#L19)
  [expression.py](Symbolic_Execution-main/PyExZ3-master/symbolic/z3_expr/expression.py#L149)

- 高：`path.smt2` 现在对“当前执行路径”是正确的，但 `path.json` 里的 `normalized_pc` 仍然不是严格意义上的路径条件，因为它丢了分支真假方向。
  相关位置：
  [normalizer.py](Symbolic_Execution-main/PyExZ3-master/symbolic/normalizer.py#L64)
  例子：`source_location_test` 的实际方向是 `[False, False]`，但 `normalized_pc` 仍是正向比较表达式，没有 `not`。

- 中：frontier 的 SMT 语义是对的，但有时会出现双重否定，读起来不干净。
  例如 `abs_test` 的 frontier 会写成 `assert (not (not (< a 0)))`。
  这在逻辑上没错，但最好再做简化。

**已确认正确的部分**
- `python -m unittest discover -s unit_tests -p "test_*.py" -v`：12/12 通过。
- `python run_tests.py test`：除 `fp.py` 外其余通过。
- script mode 基础样例可运行：
  - `test_script.py`
  - `test_script_mode.py`
  - `test_simple_script.py`
  - `test_script_complex.py`
  - `test_script_complex2.py`
- 当前路径 SMT 导出是对的：
  `outputs/abs_test/path.smt2` 现在会正确写出执行到的路径，而不是旧版那种 `asserts + not(query)`。
- 负分支也对：
  `abs_test` 首轮路径会写成 `(assert (not (< a 0)))`。
- `se` 辅助变量没有再泄漏到 `path.smt2`。
- 源码位置修正有效：
  `source_location_test` 的 `elif x < 0` 现在记录在第 7 行，不再错到第 5 行。

**所以现在能不能说“约束信息正确”**
- 可以说：`branch_trace`、`path_predicates_raw`、`path_constraints`、`path.smt2` 这几类原始约束信息，在我检查的整数/控制流样例上是正确的。
- 不能说：所有“约束相关输出”都完全正确。
  问题在于：
  - `normalized_pc`/`path_predicates_normalized` 丢失真假方向
  - 浮点相关约束链路仍不可靠

**最终判断**
- 不能通过所有测试用例。
- 不能认为“所有约束信息都已正确”。
- 但可以认为：当前版本已经把“原始路径约束导出”这条主线修到了基本可用，下一步最该补的是：
  1. `normalized_pc` 保留 `predicate.result`
  2. 浮点约束链路，先把 `fp.py` 跑通

