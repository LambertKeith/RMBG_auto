# 任务争抢修饰器
'''执行抠图之前先执行验锁上锁操作
'''
import functools

from rmbg.server import db_server
from fly_log import debug_print as print, log_time, set_log_to_file
set_log_to_file("rmbg.log")

task_locker = db_server.MySQLTaskLocker()


def image_processing_decorator(func):
    """锁处理
    在调用API抠图之前先判断该图片是否正在被处理
    """    
    @functools.wraps(func)
    def wrapper(self, image_path):
        try:
            if not task_locker.is_value_in_database(image_path):
                task_locker.insert_data(image_path)  # 添加到数据库
                print(f"正在抠图 Image {image_path} ")
                func(self, image_path)  # 执行原始方法
                task_locker.delete_data(image_path)  # 从数据库中删除
                # print(f"Image {image_path} removed from task locker.")
            else:
                print(f"Image {image_path} 正在被其他机器操作")
                pass
        except Exception as e:
            print(f"Exception processing image {image_path}: {str(e)}")
    
    return wrapper


def remove_except_lock(lock_list):
    """应对意外退出

    Args:
        lock_list (list): 上了锁的列表
    """    
    for i in lock_list:
        try:
            task_locker.delete_data(i)
        except:
            pass