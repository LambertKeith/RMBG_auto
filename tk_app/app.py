import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
from rmbg.server.app_server import AppTBGServerCaller, SingletonException
from tk_app.app_popup_window import PopupWindow



class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software with Tkinter")
        self.create_widgets()
        self.unit_progress_value = 0
        self.all_progress_value = 0
        self.popupWindow = PopupWindow(self.root)
        self.dir_path = None
        self.server_caller = None
        #self.update_progress()


    def start_matting_task(self):
        # 检查是否选择目录
        if self.dir_path == None:
            self.popupWindow.warn_popup("请选择需要操作的目录")
            return
        
        # 生成抠图功能实例
        try:
            print("创建server_caller")
            self.server_caller = AppTBGServerCaller(self.dir_path)
            print("开始抠图")
            self.server_caller.run_transparentBG()

        except SingletonException as e:
            self.popupWindow.warn_popup("每次只能操作一个文件夹！")
        
        except Exception as e:
            self.popupWindow.warn_popup("错误！请检查服务是否开启！")
        finally:
            self.server_caller = None
        

    def browse_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            print(dir_path)


    def create_widgets(self):
        """放置组件
        """        
        button_test = tk.Button(self.root, text="测试按钮", command=self.start_matting_task)
        button_test.pack(side=tk.LEFT, padx=(20, 10), pady=20)

        button_browse = tk.Button(self.root, text="目录", command=self.browse_dir)
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

        unit_increment = random.randint(0, 10)
        all_increment = random.randint(0, 5)

        self.unit_progress_value = min(self.unit_progress_value + unit_increment, 100)
        self.all_progress_value = min(self.all_progress_value + all_increment, 100)

        self.progress_unit['value'] = self.unit_progress_value
        self.progress_all['value'] = self.all_progress_value

        #self.label['text'] = f"Unit Progress: {self.unit_progress_value}% | All Progress: {self.all_progress_value}%"
        self.label['text'] = f"All Progress: {self.all_progress_value}%"

        # Reschedule the update_progress method
        self.root.after(1000, self.update_progress) # Adjust the time as necessary


    def start(self):
        self.root.after(1000, self.update_progress)  # Start the periodic update
        self.root.mainloop()


    def start_rmbg_server(self):
        """开启抠图服务
        """        
        pass


    def shut_rmbg_server(self):
        """关闭抠图服务
        """        
        pass