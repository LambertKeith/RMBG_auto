from fly_log import debug_print as print, log_time, set_log_to_file
from rmbg.server.review_server import MySQLTaskLocker
import queue
set_log_to_file("rmbg.log")



class TaskLogQueue:

    def __init__(self):
        self._queue = queue.Queue()


    def add_to_queue(self, value):
        """将参与处理的图片路径加入队列

        Args:
            value (str): 图片路径
        """        
        self._queue.put(value)


    def dequeue(self):
        if not self._queue.empty():
            return None
        else:
            return self._queue.get()


    @property
    def queue(self):
        return list(self._queue.queue)



processed_picture_queue_manager = TaskLogQueue()



class Viewer:
    def __init__(self) :
        self.task_locler = MySQLTaskLocker()
        self.task_queue_obj = processed_picture_queue_manager
        self.redistory_list = []
        self.tobe_reprocessed_list = []
    

    def check_abnormal_picture(self):
        """检查数据库里是否有
        """  
        # 获取待检查列表      
        while not self.task_queue_obj._queue.empty():
            # 获取需要检查的路径名，也就是当前实例处理过的记录
            img2be_checked = self.task_queue_obj.dequeue()
            if img2be_checked == None:
                # 当队列里处理完了，退出循环
                continue
                
            else:
                self.redistory_list.append(img2be_checked)
        
        # 循环从列表中获取
        self.tobe_reprocessed_list = [item for item in self.redistory_list 
                                      if self.task_locler.is_value_in_database(item)]
        
        # 重新调用
        # TODO


    

    

    