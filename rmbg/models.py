
import os
from queue import Queue
from rmbg.utils import get_sub_path



class FileDirectory:
    """文件夹类，用于管理和文件夹队列相关的操作
    """    
    def __init__(self, base_path):
        self.base_path = base_path
        self.folder_queue = Queue()
        self.folder_paths = []
        self.get_unit_folders()

        # 在 __init__ 方法内打印所有属性
        """ print("FileDirectory Instance variables:")
        for var, value in self.__dict__.items():
            print(f"{var}: {value}")  """       



    def get_unit_folders(self):
        """获取最小单元的目录，这一级下面就是待处理图片，
        将这些目录路径都放入队列
        # TODO
        """ 
        # 列出基础路径下的所有文件和文件夹
        items = os.listdir(self.base_path)
        # 过滤出其中的文件夹，并将它们的绝对路径保存到列表中
        for item in items:
            item_path = os.path.join(self.base_path, item)
            if os.path.isdir(item_path):
                self.folder_paths.append(item_path)  

        for i in self.folder_paths:
            self.put_folder(i)  

        self.folder_paths = []  



    def put_folder(self, folder):
        # 将一个目录放入队列
        self.folder_queue.put(folder)


    def get_folder(self):
        # 从队列中取出一个目录（如果队列为空，则返回None）
        return self.folder_queue.get() if not self.folder_queue.empty() else None



class ImgDirectory:
    """图片类
    """    
    def __init__(self, base_path):
        self.base_path = base_path
        self.img_queue = Queue()
        self.get_img_in_folder()

        # 在 __init__ 方法内打印所有属性
        """ print("ImgDirectory Instance variables:")
        for var, value in self.__dict__.items():
            print(f"{var}: {value}")   """


    def get_img_in_folder(self):
        """将目录中所有图片的路径都放入列表
        """        
        img_list = get_sub_path.get_img_path(self.base_path)
        for i in img_list:
            self.put_img(i)


    def put_img(self, img):
        # 将一个目录放入队列
        self.img_queue.put(img)


    def get_img(self):
        # 从队列中取出一个目录（如果队列为空，则返回None）
        return self.img_queue.get() if not self.img_queue.empty() else None



