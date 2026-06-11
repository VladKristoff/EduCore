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

        self.pages = {}

        self.current_window = None

    def register_page(self, name, page_class):
        self.pages[name] = page_class

    def show_window(self, name, *args, **kwargs):
        if name not in self.pages:
            print(f"Ошибка: Страница {name} не зарегистрирована!")
            return

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        page_class = self.pages[name]
        self.current_window = page_class(self.main_frame, self, *args, **kwargs)


