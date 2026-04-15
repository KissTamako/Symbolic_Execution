TODO List
=========

## 已完成的工作
- 增强了SymbolicInteger类，添加了__index__、__sizeof__、__complex__、__float__、__str__、__repr__方法
- 增强了SymbolicFloat类，添加了__index__、__sizeof__、__complex__、__str__、__repr__方法和反向比较方法
- 增强了SymbolicStr类，添加了casefold、encode、format、format_map、join、partition、rfind、rindex、rpartition、rsplit、rstrip、splitlines、swapcase、title方法
- 改进了类型转换方法，确保正确处理各种情况
- 添加了错误处理代码，确保所有方法都能正确处理错误情况

## 下一步优化方案
- add basic support for SymbolicDictionary
  - 
- need to capture exceptions thrown by code under test as test results
- interesting question arises about re-initialization of input arguments
by ExplorationEngine and re-import of module under test in the face of
mutable initial objects - we want the re-import to be done before the 
re-initialization, but that's not how it currently works. Easiest thing
to do is only allow empty dictionary to be specified in @symbolic
- check input/output behavior separately from sym_exe
- use consist case on names (Caml or C, choose one)
- 进一步增强SymbolicDictionary类，添加更多字典操作方法
- 为SymbolicRange类添加更多方法
- 优化符号执行引擎的性能
- 增加更多的测试用例，确保所有功能都能正常工作


