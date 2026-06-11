from tkinter import *
from app import AppEduCore

from view.login_page import LoginPage
from view.teacher_page import TeacherPage

if __name__ == "__main__":
    root = Tk()
    app = AppEduCore(root)

    app.register_page("login_page", LoginPage)
    app.register_page("teacher_page", TeacherPage)

    app.show_window("login_page")

    root.mainloop()
