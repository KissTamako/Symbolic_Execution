def branch_coverage(x, y):
    # 多个分支测试
    if x > 0:
        if y > 0:
            return 1  # 分支1
        else:
            return 2  # 分支2
    else:
        if y > 0:
            return 3  # 分支3
        else:
            return 4  # 分支4

def expected_result():
    return [1, 2, 3, 4]
