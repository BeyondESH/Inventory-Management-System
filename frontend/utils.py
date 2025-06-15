import tkinter as tk
from tkinter import messagebox

class Utils:
    @staticmethod
    def center_window(window, width, height):
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth-width)//2, (screenheight-height)//2)
        window.geometry(size)

    @staticmethod
    def show_info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title, message):
        messagebox.showwarning(title, message)

# 便于直接导入
center_window = Utils.center_window
show_info = Utils.show_info
show_error = Utils.show_error
show_warning = Utils.show_warning
