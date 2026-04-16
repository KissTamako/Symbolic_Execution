# 包含文件操作的学生代码测试
def read_file():
    f = open('test.txt', 'r')
    content = f.read()
    f.close()
    return content

def main():
    x = int(input())
    print(x)

if __name__ == '__main__':
    main()