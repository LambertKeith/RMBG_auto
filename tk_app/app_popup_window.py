import tkinter as tk
from tkinter import messagebox

class PopupWindow:
    def __init__(self, root):
        self.root = root
        #self.create_popup()


    def create_popup(self):
        """弹窗示例
        """        
        popup = tk.Toplevel(self.root)
        popup.title("Popup Window")
        popup.geometry("200x100")
        label = tk.Label(popup, text="This is a popup window!")
        label.pack(pady=10)
        button = tk.Button(popup, text="Close", command=popup.destroy)
        button.pack()


    def warn_popup(self, info="This is a warning popup!"):
        """警告弹窗

        Args:
            info (str, optional): 警告的信息. Defaults to "This is a warning popup!".
        """        
        messagebox.showwarning("Warning", info)