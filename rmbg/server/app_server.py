import requests
from rmbg.config.get_config import read_yaml_file
from rmbg.server.rmbg_server import TransparentBGServerCaller
from rmbg.utils import memory_lock_modifier
from rmbg.utils.rmbg_server_utils import Jpg2PngSuffix
from rmbg import models as rmbg_models


class SingletonException(Exception):
    pass



class AppTBGServerCaller(TransparentBGServerCaller):
    """APP调用抠图模块的类

    Args:
        TransparentBGServerCaller (class): 抠图父类
    """    
    _instance = None


    def __new__(cls, *args, **kwargs):
        """确保实例只会被创建一次

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """      
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise SingletonException("Singleton class should only have one instance.")
        return cls._instance


    def __init__(self, emergency_folder=None):
        # 继承原来的初始化方法
        super().__init__()
        if emergency_folder != None:
            self.emergency_folder = emergency_folder
        self.url = read_yaml_file()["rmbg"]["performance_mode_url"]
        self.total_pic_count = 0
        self.operated_pic_count = 0


    def finish_count(func):
        """完成后最后更新值

        Args:
            func: 要装饰的方法
        """        
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.operated_pic_count = self.total_pic_count
            return result
        return wrapper


    @finish_count
    def run_transparentBG(self):
        """进行抠图处理
        """    
        # 建立图片队列
        if self.emergency_folder != None:
            self.img_queue = rmbg_models.ImgDirectory(self.emergency_folder)
            self.total_pic_count = self.img_queue.img_queue.qsize()
            #print("待处理总数", self.total_pic_count)
        else:
            memory_lock_modifier.remove_except_lock(self.image_paths)    
        while True:           
            self.operation_check_Loop()
            break
        return


    def establish_img_path_list(self):
        """从队列中取出元素并加到列表中
        """   
        for _ in range(1):
            if not self.img_queue.img_queue.empty():
                img_path = self.img_queue.get_img()
                # 判断这个图片是否已经处理过
                if Jpg2PngSuffix.check_png_existence(img_path):
                    print(f"{img_path} 已完成")
                    continue
                self.image_paths.append(img_path)
            else:
                # 如果队列空了，直接退出
                break    
 

    def get_operated_count(self, func):
        """用于统计操作数量的装饰器

        Args:
            func (_type_): _description_
        """        
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self.operated_pic_count += 1
            return result
        return wrapper
    

    def process_image_local(self, image_path):
        # 将修饰器放在内部，便于传入参数
        #print("装饰器", image_path)
        @self.get_operated_count
        def inner_process_image_local(self, image_path):
            super().process_image_local(image_path)
            #print("完成率：")
            #print("待处理总数", self.total_pic_count)
            #print(self.calculate_completion_rate())

        inner_process_image_local(self, image_path)


    def calculate_completion_rate(self):
        """计算完成率

        Returns:
            int: 完成率
        """        
        if self.total_pic_count == 0:
            return 0
        print("计算完成率-数量", self.operated_pic_count)
        print("计算完成率-总数", self.total_pic_count)
        return int(self.operated_pic_count / self.total_pic_count * 1.0 * 100)    
        
            
    def test_obj(self):
        #print(1)
        super().obj_test()