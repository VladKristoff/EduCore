import tkinter as tk
from tkinter import *
from tkinter import ttk

class LoginPage:
    def __init__(self, main_frame, app):
        self.main_frame = main_frame
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        self.password_visible = tk.BooleanVar(value=False)

        ttk.Label(self.main_frame, text="EduCore", style="BigBlueLabel.TLabel").pack(side="top", pady=50)

        enter_frame = Frame(self.main_frame, background="#ffffff")
        enter_frame.pack(anchor="center", pady=100)

        enter_frame.columnconfigure(0, weight=1)

        # Логин
        ttk.Label(enter_frame, text="Логин:", style="BlueLabel.TLabel").grid(
            row=0, column=0, sticky="w", pady=(10, 0)
        )
        login_entry = ttk.Entry(enter_frame, width=20, font=("Arial", 16))
        login_entry.grid(row=1, column=0, sticky="ew", pady=(5, 15), padx=(0, 34))

        # Пароль
        ttk.Label(enter_frame, text="Пароль:", style="BlueLabel.TLabel").grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

        password_container = Frame(enter_frame, background="#ffffff")
        password_container.grid(row=3, column=0, sticky="ew", pady=(5, 20))

        password_container.columnconfigure(0, weight=1)
        password_container.rowconfigure(0, weight=1)

        # Поле ввода пароля
        password_entry = ttk.Entry(password_container, width=35, font=("Arial", 16), show="*")
        password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Кнопка-глазок
        toggle_btn = ttk.Checkbutton(
            password_container,
            text="👁",
            style="Eye.Toolbutton"
        )
        toggle_btn.grid(row=0, column=1, sticky="ns")

        # Кнопка "Войти"
        login_button = ttk.Button(enter_frame, text="Войти", style="BlueButton.TButton")
        login_button.grid(row=4, column=0, pady=20, ipady=7, ipadx=70, padx=(0, 10))


