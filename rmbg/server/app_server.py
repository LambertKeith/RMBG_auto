from rmbg.server.rmbg_server import TransparentBGServerCaller
from rmbg.utils import memory_lock_modifier
from rmbg.utils.rmbg_server_utils import Jpg2PngSuffix
from rmbg import models as rmbg_models



class AppTBGServerCaller(TransparentBGServerCaller):
    """APP调用抠图模块的类

    Args:
        TransparentBGServerCaller (class): 抠图父类
    """    
    def __init__(self, emergency_folder=None):
        # 继承原来的初始化方法
        super().__init__()
        self.emergency_folder = emergency_folder
        print("app准备完毕，待处理目录为：", self.emergency_folder)


    def run_transparentBG(self):
        """进行抠图处理
        """        
        while True:
            # 建立图片队列
            if self.emergency_folder != None:
                self.img_queue = rmbg_models.ImgDirectory(self.emergency_folder)
            else:
                memory_lock_modifier.remove_except_lock(self.image_paths)

            # 从图片对列中拿取执行
            while not self.img_queue.img_queue.empty():
                # 初始化本轮待执行列表
                if self.image_paths == []:
                    self.establish_img_path_list()
                try:
                    # 调用接口
                    self.creating_threads()
                except:
                    memory_lock_modifier.remove_except_lock(self.image_paths)
                # 清空图片列表
                self.init_image_paths()      
        

    def creating_threads(self, insert_image_paths=None):
        """建立访问线程
        """
        super().creating_threads(insert_image_paths)


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


    def test_obj(self):
        #print(1)
        super().obj_test()