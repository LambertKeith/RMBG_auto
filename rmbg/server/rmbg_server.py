
import os
import threading
import time
import requests
from rmbg.utils import jpg2png_str, get_sub_path
from rmbg.config.get_config import read_yaml_file
from rmbg import models as rmbg_models



class TransparentBGServerCaller:
    """调用API的类
    """    
    def __init__(self):
        self.url = None
        self.folder_queue = rmbg_models.FileDirectory(read_yaml_file["rmbg"]["base_path"])
        self.img_queue = None
        self.image_paths = []
        self.init_image_paths()


    def run_transparentBG(self):
        """执行调度的函数
        """      
        while True:
            # 从目录队列中取值
            folder = self.folder_queue.get_folder()

            # 判断是否为空，若空则表示结束
            if folder != None:
                # 根据每个文件夹路径生成对应的图片队列实例
                self.img_queue = rmbg_models.ImgDirectory(folder)
            else:
                return 1
            
            # 初始化队列
            if self.image_paths == []:
                self.establish_img_path_list()
            
            # 调用接口
            self.creating_threads()
            # 清空图片列表
            self.init_image_paths()


    def process_image(self, image_path):
        """调用API处理图片
        Args:
            image_path (str): 图片的路径
        """        
        try:
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
        """从队列中取出 n 个元素并加到列表中
        """        
        for _ in range(read_yaml_file()["rmbg"]["maximum_concurrent_calls"]):
            if not self.img_queue.empty():
                self.image_paths.append(self.img_queue.get())
            else:
                # 如果队列空了，直接退出
                break
    

    def init_image_paths(self):
        '''初始化图片列表
        '''
        self.image_paths = []