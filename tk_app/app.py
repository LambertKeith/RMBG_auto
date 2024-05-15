import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
from rmbg.server.app_server import AppTBGServerCaller, SingletonException
from tk_app.app_popup_window import PopupWindow
from tk_app.app_progressbar import ProgressManager



class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("赫德-白底去除工具")
        self.create_widgets()
        self.unit_progress_value = 0
        self.all_progress_value = 0

        # 初始化弹窗模块
        self.popupWindow = PopupWindow(self.root)
        # 初始化进度条模块
        self.progressManager = ProgressManager(self.root)

        self.dir_path = None
        self.server_caller = None
        self.keep_update_thread_alive = True  # 标志，进度条停止
        self.stop_matting_thread = False  # 标志，用于通知抠图线程停止
        #self.update_progress()


    def start_matting_task(self):
        """开始任务按钮响应函数
        - 启动进度条更新
        - 启动抠图功能
        - 完成后自动关闭窗口
        """        
        # 检查是否选择目录
        if self.dir_path is None:
            self.popupWindow.warn_popup("请选择需要操作的目录")
            return
        
        self.server_caller = AppTBGServerCaller(self.dir_path)
        # 传入 server_caller 用以更新进度条
        self.progressManager.update_server_caller(self.server_caller)        
        # 开始更新进度条
        # 开始更新进度条线程
        update_thread = threading.Thread(target=self.start_update_progressbar)
        update_thread.daemon = True
        update_thread.start()

        # 启动抠图线程
        matting_thread = threading.Thread(target=self._execute_matting_task)
        matting_thread.daemon = True
        matting_thread.start()


    def _execute_matting_task(self):
        try:
            # 开始操作
            self.server_caller.run_transparentBG()
            self.server_caller.operated_pic_count = self.server_caller.total_pic_count
            self.popupWindow.info_popup("运行完毕，请检查操作目录完成情况")
            print("所有任务运行完毕")
            # 停止更新进度条线程
            #self.finish_update_progressbar()
            self.root.destroy()
        except SingletonException as e:
            self.popupWindow.warn_popup("每次只能操作一个文件夹！")
        except Exception as e:
            self.popupWindow.warn_popup("错误！请检查服务是否开启！")
            import traceback; traceback.print_exc()


    def browse_dir(self):
        """选择待操作的文件夹
        """        
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            print(dir_path)
            self.progressManager.update_folder_label(dir_path)
            

    def create_widgets(self):
        """放置组件
        """        
        button_test = tk.Button(self.root, text="批量去除", command=self.start_matting_task)
        button_test.pack(side=tk.LEFT, padx=(20, 10), pady=20)

        button_browse = tk.Button(self.root, text="待操作目录", command=self.browse_dir)
        button_browse.pack(side=tk.LEFT, padx=(0, 20), pady=20)
        

    def start(self):
        """启动函数
        """        
        self.root.mainloop()


    def start_update_progressbar(self):
        """开启进度条更新
        """        
        self.progressManager.keep_update_thread_alive = True
        self.progressManager.update_progress()


    def finish_update_progressbar(self):
        """结束进度条更新
        """        
        self.progressManager.keep_update_thread_alive = False
        self.update_thread.join()


    def start_rmbg_server(self):
        """开启抠图服务
        """        
        # TODO
        pass


    def shut_rmbg_server(self):
        """关闭抠图服务
        """        
        # TODO
        pass