import os

def read_directory_contents(path):
    try:
        # 检查路径是否存在
        if not os.path.exists(path):
            print("指定路径不存在。")
            return

        # 检查路径是否为目录
        if not os.path.isdir(path):
            print("指定路径不是一个目录。")
            return

        # 获取目录下所有内容
        contents = os.listdir(path)

        # 打印内容
        print("目录内容:")
        for item in contents:
            print(item)

    except Exception as e:
        print(f"发生错误: {e}")

# 测试方法
path = r"\\192.168.10.229\摄影部\千百度男鞋"
read_directory_contents(path)
