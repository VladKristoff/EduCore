from tkinter import *
from app import AppEduCore

from view.login_page import LoginPage

if __name__ == "__main__":
    root = Tk()
    app = AppEduCore(root)

    app.show_window(LoginPage)

    root.mainloop()
