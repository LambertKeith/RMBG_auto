import os
import shutil
from rmbg.config.get_config import read_yaml_file
from rmbg.utils import jpg2png_str, get_sub_path
from rmbg import models as rmbg_models


def test1():
    print(jpg2png_str.convert_extension("1.2.3.jpg"))


def test2():
    
    print(read_yaml_file()["rmbg"]["maximum_concurrent_calls"])
    pass


def test3():
    folders = rmbg_models.FileDirectory("21312")
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



if __name__ == "__main__":
    test4()
    pass