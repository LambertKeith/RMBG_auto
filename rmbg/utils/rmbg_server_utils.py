
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