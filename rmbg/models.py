
import os
from queue import Queue
from rmbg.utils import get_sub_path
from rmbg.config import get_config



class FileDirectory:
    """文件夹类，用于管理和文件夹队列相关的操作
    """    
    def __init__(self, base_path=''):
        #self.base_path = base_path
        self.base_path ="\\\\192.168.10.229\\图片\\批量抠图"
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
        步骤：
        - 通过读取配置文件，锁定本机需要处理的品牌文件夹，并组合为绝对路径
        - 轮流遍历这些绝对路径，将其中的子文件夹绝对路径直接加入队列
        """ 
        # 获取当前app_id
        app_id = get_config.read_yaml_file()["rmbg"]["app_id"]
        # 通过id获得本实例分配的品牌文件夹
        brand_folder_list = get_config.brand_folder[app_id]
        # 组合为绝对路径
        brand_folder_absolute_path_list = [os.path.join(self.base_path, brand_folder) for brand_folder in brand_folder_list]
        #print(brand_folder_absolute_path_list)
        
        # 遍历每个品牌文件夹路径
        for folder_path in brand_folder_absolute_path_list:
            try:
                # 重新用gbk编码
                #folder_path = folder_path.encode('gbk')
                # 检查路径是否存在且是一个目录
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    # 获取文件夹下的所有一级子目录（文件夹）
                    subfolders = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

                    # 将路径放入队列
                    for subfolder in subfolders:
                        #print(os.path.join(folder_path, subfolder))
                        self.put_folder(subfolder)
                else:
                    print(f"Error: {folder_path} is not a valid directory or does not exist.")   

            except Exception as e:
                import traceback; traceback.print_exc();    


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



