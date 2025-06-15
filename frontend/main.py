import tkinter as tk
from login import LoginUI
from menu import MainMenuUI
from utils import center_window

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("食品服务公司管理系统")
        self.root.geometry("900x600")
        center_window(self.root, 900, 600)
        self.current_frame = None
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginUI(self.root, self.on_login_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user_info):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainMenuUI(self.root, user_info)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
