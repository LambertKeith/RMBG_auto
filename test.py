from rmbg.config.get_config import read_yaml_file
from rmbg.utils import jpg2png_str
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

if __name__ == "__main__":
    test3()
    pass