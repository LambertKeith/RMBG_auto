import tkinter as tk

class ButtonManager:
    def __init__(self, root, text="Button", command=None, bg="lightgray", fg="black", side=None, padx=None, pady=None):
        self.root = root
        self.text = text
        self.command = command
        self.bg = bg
        self.fg = fg
        self.button = None

        self.style_dict = {
            "side": side, 
            "padx": padx, 
            "pady": pady, 
        }

    def create_button(self):
        self.button = tk.Button(self.root, text=self.text, command=self.command, bg=self.bg, fg=self.fg)
        self.button.pack(side=self.style_dict["side"], padx=self.style_dict["padx"], pady=self.style_dict["pady"])

    def set_text(self, new_text):
        if self.button:
            self.button.config(text=new_text)
        self.text = new_text

    def set_command(self, new_command):
        if self.button:
            self.button.config(command=new_command)
        self.command = new_command

    def set_bg_color(self, color):
        if self.button:
            self.button.config(bg=color)
        self.bg = color

    def set_fg_color(self, color):
        if self.button:
            self.button.config(fg=color)
        self.fg = color

    def disable(self):
        if self.button:
            self.button.config(state=tk.DISABLED)

    def enable(self):
        if self.button:
            self.button.config(state=tk.NORMAL)


