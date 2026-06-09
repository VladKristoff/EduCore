from tkinter import *

class AppEduCore:
    def __init__(self, root):
        self.root = root
        root.title("EduCore")
        root.geometry("1600x900")
        root.resizable(False, False)

        self.main_frame = Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.icon = PhotoImage(file='images/logo.png')
        root.iconphoto(True, self.icon)

        self.current_window = None

    def show_window(self, page_class, *args, **kwargs):
        if self.current_window:
            self.current_window.destroy()

        self.current_window = page_class(self.main_frame, self, *args, **kwargs)
