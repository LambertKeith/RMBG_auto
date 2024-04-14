# 任务争抢修饰器
'''执行抠图之前先执行验锁上锁操作
'''
import functools

from rmbg.server import db_server

task_locker = db_server.MySQLTaskLocker()


def image_processing_decorator(func):
    @functools.wraps(func)
    def wrapper(self, image_path):
        try:
            if not task_locker.is_value_in_database(image_path):
                task_locker.insert_data(image_path)  # 添加到数据库
                print(f"Image {image_path} added to task locker.")
                func(self, image_path)  # 执行原始方法
                task_locker.delete_data(image_path)  # 从数据库中删除
                print(f"Image {image_path} removed from task locker.")
            else:
                print(f"Image {image_path} already in task locker. Skipping processing.")
                pass
        except Exception as e:
            print(f"Exception processing image {image_path}: {str(e)}")
    
    return wrapper