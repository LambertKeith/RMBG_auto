import os
import shutil
from rmbg.config.get_config import read_yaml_file, brand_folder
from rmbg.server.db_server import MySQLTaskLocker
from rmbg.utils import jpg2png_str, get_sub_path
from rmbg import models as rmbg_models


def test1():
    print(jpg2png_str.convert_extension("1.2.3.jpg"))


def test2():
    show_info = read_yaml_file()["rmbg"]["base_path"]
    print(show_info)
    pass


def test3():
    # folders = rmbg_models.FileDirectory(r"\\192.168.10.229\图片\批量抠图")
    folders = rmbg_models.FileDirectory(r"test_folder")
    flag = True
    while flag:
        i = folders.get_folder()
        if i !=None:
            print(i)
        else:
            flag = False


def test4():
    path_list = get_sub_path.get_img_path(r"\\192.168.10.229\摄影部\千百度男鞋\商务\2024\4月\4.8 白底\C0142150LA73")
    print(path_list)
    def copy_file_to_current_directory(source_path):
        if os.path.isfile(source_path):
            shutil.copy(source_path, os.path.join(os.getcwd(), os.path.basename(source_path)))
            print("File copied successfully.")
        else:
            print("Error: Source path is not a file.")
    copy_file_to_current_directory(path_list[5])


def test5():
    app_id = read_yaml_file()["rmbg"]["app_id"]
    print(brand_folder[app_id])

def test6():
    import os

    # 存放文件夹路径的列表
    brand_folder_absolute_path_list = [
        "\\\\192.168.10.229\\图片\\批量抠图\\伊伴翔鹏",
        "\\\\192.168.10.229\\图片\\批量抠图\\千百度休闲",
        "\\\\192.168.10.229\\图片\\批量抠图\\笑脸"
    ]

    # 遍历每个文件夹路径
    for folder_path in brand_folder_absolute_path_list:
        # 检查路径是否存在且是一个目录
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # 获取文件夹下的所有一级子目录（文件夹）
            subfolders = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
            # 打印子目录的绝对路径
            print(f"Subfolders in {folder_path}:")
            for subfolder in subfolders:
                print(subfolder)
        else:
            print(f"Error: {folder_path} is not a valid directory or does not exist.")


def test7():
    import os

    def count_png_files(directory):
        count = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.jpg'):
                    count += 1
        return count

    # Example usage:
    directory = r"\\192.168.10.229\图片\千百度男鞋\休闲\未完成\待抠"
    png_count = count_png_files(directory)
    print(f'Total number of PNG files: {png_count}')


def test8():
    from datetime import datetime

    def calculate_time_interval(start_time, end_time):
        # 将时间字符串转换为datetime对象
        start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        # 计算时间间隔
        time_interval = end_datetime - start_datetime

        # 将时间间隔转换为小时
        hours = time_interval.total_seconds() / 3600

        return hours

    # Example usage:
    start_time = '2024-04-11 15:50:00'
    end_time = '2024-04-11 17:07:00'
    interval_hours = calculate_time_interval(start_time, end_time)
    print(f'Time interval: {interval_hours} hours')


def test9():
    import os

    def check_png_existence(img_path):
        # 检查文件扩展名是否为.jpg或.jpeg
        if img_path.endswith(('.jpg', '.jpeg')):
            # 从文件路径中分离出基本文件名和目录
            base_path, extension = os.path.splitext(img_path)
            # 更改扩展名为.png
            png_path = base_path + '.png'
            # 检查png文件是否存在
            return os.path.exists(png_path)
        else:
            return False  # 如果文件扩展名不是.jpg或.jpeg，返回False

    # 使用示例
    img_path = r'test_folder\folder2\D-8E9A7131.jpg'
    exists = check_png_existence(img_path)
    print(f"Does a PNG version exist? {'Yes' if exists else 'No'}")


def test10():
    # Example Usage:
    # Replace 'your_host', 'your_database' with your actual host and database names
    connector = MySQLTaskLocker()

    # Example: Inserting data
    #connector.insert_data("example_picture.jpg")

    # Example: Deleting data
    #connector.delete_data("example_picture.jpg")
    print(connector.is_value_in_database("example_picture1.jpg"))
    



if __name__ == "__main__":
    test10()
    pass