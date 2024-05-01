import os



class RmbgServerManager:
    """用于开启和关闭抠图服务
    """    
    def __init__(self) -> None:
        self.worker_count = None
        self.server_path = self.composite_service_startup_path()
        #print(self.server_path)
        


    def composite_service_startup_path(self):
        """生成服务启动地址
        """        

        # 获取当前工作目录的上一级目录路径
        parent_dir = os.path.dirname(os.getcwd())

        # 目录名为 transparent-background
        folder_name = "transparent-background"

        # 组合新的路径
        new_path = os.path.join(parent_dir, folder_name)

        #print("新路径:", new_path)
        return new_path

