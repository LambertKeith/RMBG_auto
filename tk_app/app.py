import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
from rmbg.server.app_server import AppTBGServerCaller, SingletonException
from tk_app.app_popup_window import PopupWindow



class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("赫德-白底去除工具")
        self.create_widgets()
        self.unit_progress_value = 0
        self.all_progress_value = 0
        self.popupWindow = PopupWindow(self.root)
        self.dir_path = None
        self.server_caller = None
        self.keep_update_thread_alive = True  # 标志，进度条停止
        self.stop_matting_thread = False  # 标志，用于通知抠图线程停止
        #self.update_progress()


    def start_matting_task(self):
        # 检查是否选择目录
        if self.dir_path == None:
            self.popupWindow.warn_popup("请选择需要操作的目录")
            return
        
        # 启动抠图线程
        matting_thread = threading.Thread(target=self._execute_matting_task)
        matting_thread.start()

        # 等待抠图线程执行完毕
        matting_thread.join()

        # 抠图线程执行完毕后，设置标志通知线程停止
        self.stop_matting_thread = True


    def _execute_matting_task(self):
        try:
            self.server_caller = AppTBGServerCaller(self.dir_path)
            self.server_caller.run_transparentBG()
        except SingletonException as e:
            self.popupWindow.warn_popup("每次只能操作一个文件夹！")
        except Exception as e:
            self.popupWindow.warn_popup("错误！请检查服务是否开启！")
            import traceback; traceback.print_exc()
        finally:
            self.server_caller.operated_pic_count = self.server_caller.total_pic_count
            #self.server_caller = None
            # 备用 2024.5.4
            """ if self.server_caller is not None:
                self.server_caller.release_resources()
                self.server_caller = None """
        

    def browse_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            print(dir_path)


    def create_widgets(self):
        """放置组件
        """        
        button_test = tk.Button(self.root, text="批量去除", command=self.start_matting_task)
        button_test.pack(side=tk.LEFT, padx=(20, 10), pady=20)

        button_browse = tk.Button(self.root, text="待操作目录", command=self.browse_dir)
        button_browse.pack(side=tk.LEFT, padx=(0, 20), pady=20)

        module_frame = tk.Frame(self.root)
        module_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.label = tk.Label(module_frame, text="Ready", height=2)
        self.label.pack(fill=tk.X)

        self.progress_unit = ttk.Progressbar(module_frame, length=100)
        #self.progress_unit.pack(fill=tk.X)

        self.progress_all = ttk.Progressbar(module_frame, length=100)
        self.progress_all.pack(fill=tk.X)


    def update_progress(self):
        """更新进度条
        # TODO
        """     

        while True:  # 无限循环以持续更新进度条
            try:
                
                while self.keep_update_thread_alive:  # 当标志为 True 时保持运行
                    
                    if self.server_caller is not None:
                        #print("Updating progress...")
                        unit_increment = random.randint(0, 10)
                        all_increment = random.randint(0, 5)

                        self.unit_progress_value = min(self.unit_progress_value + unit_increment, 100)
                        self.all_progress_value = min(self.all_progress_value + all_increment, 100)

                        #print(f"Unit Progress: {self.unit_progress_value}, All Progress: {self.all_progress_value}")

                        self.progress_unit['value'] = self.unit_progress_value
                        self.progress_all['value'] = self.server_caller.calculate_completion_rate()

                    self.label['text'] = f"总进度：{self.progress_all['value']}%"

                    time.sleep(1)
            except:
                print("update_progress error")
        

    def start(self):
        # 在新线程中启动更新进度条的方法
        update_thread = threading.Thread(target=self.update_progress)
        update_thread.start()

        self.root.mainloop()

        # 退出应用程序时，设置退出标志，关闭子线程
        self.keep_update_thread_alive = False
        update_thread.join()  # 等待子线程结束


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