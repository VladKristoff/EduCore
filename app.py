from tkinter import *
from styles import set_style

class AppEduCore:
    def __init__(self, root):
        self.root = root
        root.title("EduCore")
        root.geometry("1440x810")
        root.resizable(False, False)

        self.main_frame = Frame(root, background="#ffffff")
        self.main_frame.pack(fill="both", expand=True)

        self.icon = PhotoImage(file='images/logo.png')
        root.iconphoto(True, self.icon)

        set_style(self.root)

        self.current_window = None

    def show_window(self, page_class, *args, **kwargs):
        if self.current_window:
            self.current_window.destroy()

        self.current_window = page_class(self.main_frame, self, *args, **kwargs)
