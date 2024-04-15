
import os
import threading
import time
import requests
from rmbg.utils import jpg2png_str, get_sub_path, memory_lock_modifier
from rmbg.config.get_config import read_yaml_file
from rmbg import models as rmbg_models
from fly_log import debug_print as print, log_time, set_log_to_file
from rmbg.server import db_server
set_log_to_file("rmbg.log")



class TransparentBGServerCaller:
    """调用API的类
    """    
    def __init__(self):
        self.url = read_yaml_file()["rmbg"]["transparentBG_server_url"]
        self.shutdown_url = read_yaml_file()["rmbg"]["shutdown_server_url"]
        self.folder_queue = rmbg_models.FileDirectory(read_yaml_file()["rmbg"]["base_path"])
        self.img_queue = None
        self.image_paths = []
        self.init_image_paths()

        # 在 __init__ 方法内打印所有属性
        """ print("TransparentBGServerCaller Instance variables:")
        for var, value in self.__dict__.items():
            print(f"{var}: {value}")  """


    def run_transparentBG(self):
        """执行调度的函数
        """      
        while True:
            
            # 从目录队列中取值
            folder = self.folder_queue.get_folder()
            print(f"=========={folder}==========")

            # 判断是否为空，若空则表示结束
            if folder != None:
                # 根据每个文件夹路径生成对应的图片队列实例
                self.img_queue = rmbg_models.ImgDirectory(folder)
            else:
                if read_yaml_file()["rmbg"]["Automatic_shutdown"]:
                    self.shutdown_server()
                return True
            
            while not self.img_queue.img_queue.empty():
                
                # 初始化队列
                if self.image_paths == []:
                    self.establish_img_path_list()
                try:
                    # 调用接口
                    self.creating_threads()
                except:
                    memory_lock_modifier.remove_except_lock(self.image_paths)
                # 清空图片列表
                self.init_image_paths()




    @memory_lock_modifier.image_processing_decorator
    def process_image(self, image_path):
        """调用API处理图片
        Args:
            image_path (str): 图片的路径
        """        
        try:
            print(f"Image {image_path} 正在操作")
            with open(image_path, "rb") as f:
                response = requests.post(self.url, files={"file": f})
            
            if response.status_code == 200:
                #output_filename = f"{os.path.basename(image_path)}".split('.jpg')[0] + ".png"
                # 将处理好的文件放到原来的路径下，保存为png
                output_filename = jpg2png_str.convert_extension(image_path)
                with open(output_filename, "wb") as output_file:
                    output_file.write(response.content)
                print(f"Image {image_path} processed successfully. Processed image saved as {output_filename}")
            else:
                print(f"Error processing image {image_path}: {response.text}")
        except Exception as e:
            print(f"Exception processing image {image_path}: {str(e)}")
    

    def creating_threads(self):
        """建立访问线程
        """
        # 创建线程列表
        threads = []

        # 启动线程调用处理函数
        for image_path in self.image_paths:
            thread = threading.Thread(target=self.process_image, args=(image_path,))
            threads.append(thread)
            thread.start()

        # 等待所有线程结束
        for thread in threads:
            thread.join()

        print("All images processed.")


    def establish_img_path_list(self):
        """从队列中取出元素并加到列表中
        """        
        for _ in range(read_yaml_file()["rmbg"]["maximum_concurrent_calls"]):
            if not self.img_queue.img_queue.empty():
                img_path = self.img_queue.get_img()

                # 判断这个图片是否已经处理过
                if self.check_png_existence(img_path):
                    print(f"{img_path} has been manipulated")
                    continue
                self.image_paths.append(img_path)
            else:
                # 如果队列空了，直接退出
                break
    

    def init_image_paths(self):
        '''初始化图片列表
        '''
        self.image_paths = []


    def check_png_existence(self, img_path):
        """检查图片是否已经被处理

        Args:
            img_path (_type_): 待检测图片的路径

        Returns:
            _type_: _description_
        """        
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


    def shutdown_server(self):
        try:
            response = requests.post(self.shutdown_url)
            if response.status_code == 200:
                print("服务器已关闭")
            else:
                print("无法关闭服务器，状态码:", response.status_code)
        except Exception as e:
            print("发生错误:", e)