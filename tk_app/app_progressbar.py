import threading
import time
import tkinter as tk
from tkinter import ttk
import random



class ProgressManager:
    def __init__(self, root, server_caller=None):
        self.root = root
        self.unit_progress_value = 0
        self.all_progress_value = 0
        self.keep_update_thread_alive = True
        self.server_caller = None
        self.update_server_caller(server_caller)
        self.create_progress_widgets()


    def create_progress_widgets(self):
        """创建进度条组件"""
        module_frame = tk.Frame(self.root)
        module_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.folder_label = tk.Label(module_frame, text="", height=2)
        self.folder_label.pack(fill=tk.X)
        self.label = tk.Label(module_frame, text="Ready", height=2)
        self.label.pack(fill=tk.X)

        self.progress_unit = ttk.Progressbar(module_frame, length=100)
        # self.progress_unit.pack(fill=tk.X)

        self.progress_all = ttk.Progressbar(module_frame, length=100)
        self.progress_all.pack(fill=tk.X)


    def update_progress(self):
        """更新进度条"""
        if self.keep_update_thread_alive:
            try:
                if self.server_caller is not None:
                    self.progress_unit['value'] = self.unit_progress_value
                    self.all_progress_value = self.server_caller.calculate_completion_rate()
                    self.progress_all['value'] = self.all_progress_value
                    self.label['text'] = f"总进度：{self.all_progress_value}%"

                    # 如果加载完成则停止更新
                    if self.all_progress_value >= 100:
                        self.keep_update_thread_alive = False
                        return

                # 使用 after 方法安排下一次更新
                if self.keep_update_thread_alive:
                    self.root.after(1000, self.update_progress)

            except Exception as e:
                print(f"update_progress error: {e}")
                self.keep_update_thread_alive = False


    def update_server_caller(self, server_caller):
        """更新server_caller

        Args:
            server_caller (): _description_
        """        
        self.server_caller = server_caller
    

    def update_folder_label(self, folder_name):
        """显示待操作文件名

        Args:
            folder_name (str): 待操作的文件名
        """        
        self.folder_label['text'] = folder_name