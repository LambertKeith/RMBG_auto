
import os
import threading
import time
import requests
from rmbg.utils import jpg2png_str
from rmbg.config.get_config import read_yaml_file



class TransparentBGServerCaller:
    """调用API的类
    """    
    def __init__(self):
        self.url = None
        self.folder_queue = None
        self.img_queue = None


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
                break
    

    def init_image_paths(self):
        '''初始化图片列表
        '''
        self.image_paths = []