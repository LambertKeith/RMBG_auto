
import os
import threading
import time
import requests
from rmbg.utils import get_sub_path, memory_lock_modifier
from rmbg.config.get_config import read_yaml_file
from rmbg import models as rmbg_models

from rmbg.server import db_server
from fly_log import debug_print as print, log_time, set_log_to_file
from queue import Queue
from rmbg.utils.rmbg_server_utils import Jpg2PngSuffix
from rmbg.utils.rmbg_server_utils import timer
set_log_to_file("rmbg.log")



class TransparentBGServerCaller:
    """调用API的类
    """    
    def __init__(self, folder_queue=None):
        self.url = read_yaml_file()["rmbg"]["transparentBG_server_url"]
        self.shutdown_url = read_yaml_file()["rmbg"]["shutdown"]["shutdown_server_url"]
        self.folder_queue = rmbg_models.FileDirectory(read_yaml_file()["rmbg"]["base_path"])
        self.img_queue = None
        self.check_queue = Queue()
        self.image_paths = []

        # self.processed_picture_list = []
        self.init_image_paths()

        # 在 __init__ 方法内打印所有属性
        """ print("TransparentBGServerCaller Instance variables:")
        for var, value in self.__dict__.items():
            print(f"{var}: {value}")  """


    def run_transparentBG(self):
        """执行调度的函数
        """      
        """ for item in list(self.folder_queue.folder_queue.queue):
            print(item) """
        while True:
            
            # 从目录队列中取值
            folder = self.folder_queue.get_folder()
            print(f"===================={folder}====================")

            # 判断是否为空，若空则表示结束
            if folder != None:
                
                # 根据每个文件夹路径生成对应的图片队列实例
                self.img_queue = rmbg_models.ImgDirectory(folder)
            else:

                memory_lock_modifier.remove_except_lock(self.image_paths)
                # print(f"self.image_paths: {self.image_paths}")
                if read_yaml_file()["rmbg"]["shutdown"]["Automatic_shutdown"]:
                    self.shutdown_server()
                
                return True
            if self.operation_check_Loop() == 0:
                return
            """ while not self.img_queue.img_queue.empty():
                # 初始化本轮待执行列表
                if self.image_paths == []:
                    self.establish_img_path_list()
                try:
                    # 调用接口
                    self.creating_threads()
                except:
                    memory_lock_modifier.remove_except_lock(self.image_paths)
                # 清空图片列表
                self.init_image_paths() """


    def operation_check_Loop(self): 
        """操作检查循环
        操作完成一轮后自动检查
        """        
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

        # 进行检查,递归调用
        print("开始检查")
        if not self.check_queue.empty():
            self.img_queue.img_queue = self.check_queue  
            self.operation_check_Loop()
        else:
            print("当前文件夹下所有jpg操作完毕")
            return 0

    
    @memory_lock_modifier.image_processing_decorator
    def process_image(self, image_path):
        """调用API处理图片
        Args:
            image_path (str): 图片的路径
        """        
        try:
            #print(f"Image {image_path} 正在操作")
            with open(image_path, "rb") as f:
                response = requests.post(self.url, files={"file": f})
            # print(f"Image {image_path} requests success")
            
            if response.status_code == 200:
                #output_filename = f"{os.path.basename(image_path)}".split('.jpg')[0] + ".png"
                # 将处理好的文件放到原来的路径下，保存为png
                output_filename = Jpg2PngSuffix.convert_extension(image_path)
                with open(output_filename, "wb") as output_file:
                    output_file.write(response.content)
                print(f"Image {image_path} 操作完成.")
            else:
                print(f"Error processing image {image_path}: {response.text}")
        except Exception as e:
            print(f"Exception processing image {image_path}: {str(e)}")


    @memory_lock_modifier.image_processing_decorator
    def process_image_local(self, image_path):
        """调用API处理图片
        Args:
            image_path (str): 图片的路径
        """        
        try:
            #print(f"Image {image_path} 正在操作")
            output_filename = Jpg2PngSuffix.convert_extension(image_path)

            response = requests.post(
                self.url,
                params={"input_path": f"{image_path}", "output_path": f"{output_filename}"}
            )
            if response.status_code == 200:
                print(f"Image {image_path} 操作完成.")
            else:
                print(f"Error processing image {image_path}: {response.text}")
        except Exception as e:
            print(f"Exception processing image {image_path}: {str(e)}")
    

    def creating_threads(self, insert_image_paths=None):
        """建立访问线程
        """
        # 创建线程列表
        threads = []
        if insert_image_paths == None:
            image_paths = self.image_paths
        else:
            image_paths = insert_image_paths
        
        # 启动线程调用处理函数
        for image_path in image_paths:
            try:
            
                #thread = threading.Thread(target=self.process_image, args=(image_path,))
                thread = threading.Thread(target=self.process_image_local, args=(image_path,))
                threads.append(thread)
                thread.start()
            except Exception as e:
                import traceback; traceback.print_exc();
                print("error")

        # 等待所有线程结束
        for thread in threads:
            thread.join()

        # print("All images processed.")


    def establish_img_path_list(self):
        """从队列中取出元素并加到列表中
        """        
        for _ in range(read_yaml_file()["rmbg"]["maximum_concurrent_calls"]):
            if not self.img_queue.img_queue.empty():
                img_path = self.img_queue.get_img()
                self.check_queue.put(img_path)

                # 判断这个图片是否已经处理过
                if Jpg2PngSuffix.check_png_existence(img_path):
                    print(f"{img_path} 已完成")
                    [print("Processing item:", self.check_queue.get()) if not self.check_queue.empty() else None]
                    continue
                
                self.image_paths.append(img_path)
            else:
                # 如果队列空了，直接退出
                break
    

    def init_image_paths(self):
        '''初始化图片列表
        '''
        self.image_paths = []


    def shutdown_server(self):
        """关机
        如果达到指定时间且程序执行完毕，则调用服务关机
        """     
        if not Jpg2PngSuffix.is_off_work():    
            print("现在还没有到关机时间")
            return 0  
        try:
            print("正在关机")
            response = requests.post(self.shutdown_url)
            if response.status_code == 200:
                print("服务器已关闭")
            else:
                print("无法关闭服务器，状态码:", response.status_code)
        except Exception as e:
            print("发生错误:", e)
        
    
    def obj_test(self):
        """测试方法
        """        
        print("Hey, I'm TransparentBGServerCaller")