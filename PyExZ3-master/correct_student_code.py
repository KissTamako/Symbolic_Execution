#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
正确的学生代码示例 - 质数回文数检测

这是一个语法正确、逻辑完整的学生作业代码示例。
功能：找出2到N之间的所有质数回文数
"""

def isPrime(n):
    """判断一个数是否为质数"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # 检查从3到sqrt(n)的奇数因子
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def reverseNumber(n):
    """判断一个数是否为回文数"""
    str_n = str(n)
    return str_n == str_n[::-1]

# 主程序 - 获取用户输入并计算结果
def main():
    try:
        # 获取用户输入
        n = int(input("请输入一个正整数N: "))
        
        # 输入验证
        if n < 2:
            print("输入必须大于等于2")
            return
        
        result = []
        # 找出2到n之间的所有质数回文数
        for i in range(2, n + 1):
            if isPrime(i) and reverseNumber(i):
                result.append(i)
        
        # 输出结果
        if result:
            print(f"在2到{n}之间的质数回文数有: {result}")
            print(f"共有 {len(result)} 个质数回文数")
        else:
            print(f"在2到{n}之间没有质数回文数")
            
    except ValueError:
        print("输入错误：请输入一个整数")
    except Exception as e:
        print(f"程序出错: {e}")

# 提供一个简单的测试函数，便于验证
def test_with_value(N):
    """测试函数，用于验证代码逻辑"""
    if N < 2:
        return []
    
    result = []
    for i in range(2, N + 1):
        if isPrime(i) and reverseNumber(i):
            result.append(i)
    return result

if __name__ == "__main__":
    main()