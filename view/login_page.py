import tkinter as tk
from tkinter import *
from tkinter import ttk
from database.db_manager import db_manager

class LoginPage:
    def __init__(self, main_frame, app):
        self.main_frame = main_frame
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        self.password_visible = tk.BooleanVar(value=False)

        ttk.Label(self.main_frame, text="EduCore", style="BigBlueLabel.TLabel").pack(side="top", pady=50)

        enter_frame = Frame(self.main_frame, background="#ffffff")
        enter_frame.pack(anchor="center", pady=(100, 0))

        enter_frame.columnconfigure(0, weight=1)

        # Логин
        ttk.Label(enter_frame, text="Логин:", style="BlueLabel.TLabel").grid(
            row=0, column=0, sticky="w", pady=(10, 0)
        )
        self.username_entry = ttk.Entry(enter_frame, width=20, font=("Arial", 16))
        self.username_entry.grid(row=1, column=0, sticky="ew", pady=(5, 15), padx=(0, 34))

        # Пароль
        ttk.Label(enter_frame, text="Пароль:", style="BlueLabel.TLabel").grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

        password_container = Frame(enter_frame, background="#ffffff")
        password_container.grid(row=3, column=0, sticky="ew", pady=(5, 20))

        password_container.columnconfigure(0, weight=1)
        password_container.rowconfigure(0, weight=1)

        # Поле ввода пароля
        self.password_entry = ttk.Entry(password_container, width=35, font=("Arial", 16), show="*")
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Кнопка-глазок
        toggle_btn = ttk.Checkbutton(
            password_container,
            text="👁",
            style="Eye.Toolbutton",
            variable=self.password_visible,
            command=lambda: self.toggle_password_visible()
        )
        toggle_btn.grid(row=0, column=1, sticky="ns")

        # Кнопка "Войти"
        login_button = ttk.Button(enter_frame, text="Войти", style="BlueButton.TButton",
                                  command=lambda: self.authorization())
        login_button.grid(row=4, column=0, pady=20, ipady=7, ipadx=70, padx=(0, 10))

        self.error_label = ttk.Label(self.main_frame, text="Введите логин и пароль",
                                style="ErrorLabel.TLabel")
        self.error_label.pack(side="top")

    def toggle_password_visible(self):
        if self.password_visible.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def authorization(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(foreground="red")
            return
        else:
            role = db_manager.authenticate_user(username, password)
            if role == "app":
                self.app.show_window("teacher_page")
            elif role == "admin":
                self.app.show_window("admin_page")
            else:
                print("Ошибка открытия страницы пользователя")

