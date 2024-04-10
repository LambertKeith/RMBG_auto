import os
import shutil
from rmbg.config.get_config import read_yaml_file, brand_folder
from rmbg.utils import jpg2png_str, get_sub_path
from rmbg import models as rmbg_models


def test1():
    print(jpg2png_str.convert_extension("1.2.3.jpg"))


def test2():
    
    print(read_yaml_file()["rmbg"]["test_item"][0])
    pass


def test3():
    folders = rmbg_models.FileDirectory(r"\\192.168.10.229\图片\批量抠图")
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

if __name__ == "__main__":
    test6()
    pass