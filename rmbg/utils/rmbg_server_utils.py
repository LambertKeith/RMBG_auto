
import os
from rmbg.config import get_config
import datetime


class Jpg2PngSuffix:

    
    start_hour = get_config.read_yaml_file()["rmbg"]["shutdown"]["OffTime"][0]
    end_hour = get_config.read_yaml_file()["rmbg"]["shutdown"]["OffTime"][1]
        

    def convert_extension(filename):
        """将后缀为jpg、jpeg、JPG或者JPEG的字符串转换为png结尾的字符串

        Args:
            filename (str): 尾缀为jpg、jpeg、JPG或者JPEG的文件名

        Returns:
            str: 转换后的文件名，以png结尾
        """    
        
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            index = filename.lower().rfind('.jpg')  # 找到最后一个'.jpg'的索引
            if index == -1:  # 如果未找到'.jpg'，则查找'.jpeg'
                index = filename.lower().rfind('.jpeg')
            return filename[:index] + '.png'  # 替换为'.png'
        else:
            return filename  # 如果不是jpg、jpeg、JPG或JPEG结尾的文件名，则不做修改

        

    def is_off_work(start_hour=start_hour, end_hour=end_hour, start_minute=0, end_minute=0):
        """判断当前是否处于工作时间段
        为了传参方便暂时放这里
        后面这个模块需要转移到其他类、
        # TODO

        Args:
            start_hour (int, optional): 下班开始时间. Defaults to start_hour.
            end_hour (int, optional): 下班结束时间. Defaults to end_hour.
            start_minute (int, optional): _description_. Defaults to 0.
            end_minute (int, optional): _description_. Defaults to 0.

        Returns:
            bool: 如果是非工作时间段则输出True
        """        
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(start_hour, start_minute)  # 下班开始时间
        end_time = datetime.time(end_hour, end_minute)  # 下班结束时间
        
        if current_time >= start_time or current_time < end_time:
            return True
        else:
            return False


    def check_png_existence(img_path):
        """检查图片是否已经被处理

        Args:
            img_path (str): 待检测图片的路径

        Returns:
            bool: 如果已经存在以.png结尾的图片则返回True，否则返回False
        """        
        # 检查文件扩展名是否为.jpg、.jpeg、.JPG或.JPEG
        if img_path.lower().endswith(('.jpg', '.jpeg', '.jpg', '.jpeg')):
            # 从文件路径中分离出基本文件名和目录
            base_path, _ = os.path.splitext(img_path)
            # 更改扩展名为.png
            png_path = base_path + '.png'
            # 检查png文件是否存在
            return os.path.exists(png_path)
        else:
            return False  # 如果文件扩展名不是.jpg、.jpeg、.JPG或.JPEG，返回False
