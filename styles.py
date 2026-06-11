from tkinter import *
from tkinter import ttk

def set_style(root):
    style = ttk.Style(root)

    style.theme_use("clam")

    # Большая синяя надпись
    style.configure("BigBlueLabel.TLabel",
                    foreground="#279ef9",
                    font=("Inter", 48, "bold"),
                    background="#ffffff")

    # Обычная синяя надпись
    style.configure("BlueLabel.TLabel",
                    foreground="#279ef9",
                    font=("Inter", 24, "bold"),
                    background="#ffffff")

    # Надпись ошибки
    style.configure("ErrorLabel.TLabel",
                    foreground="#ffffff",
                    background="#ffffff",
                    font=("Arial", 16))

    # Синяя кнопка
    style.configure("BlueButton.TButton",
                    background="#279ef9",
                    foreground="#ffffff",
                    font=("Inter", 20, "bold"),
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor="none",
                    relief="flat")

    style.map("BlueButton.TButton",
              background=[
                  ('pressed', '#006BFF'),
                  ('active', '#006BFF')
              ],
              foreground=[
                  ('pressed', 'white'),
                  ('active', 'white')
              ])

    # Кнопка в виде глазика
    style.configure(
        "Eye.Toolbutton",
        font=("Arial", 14),
        foreground="#1e3d59",
        background="#ffffff",
        padding=5,
        borderwidth=0,
        focusthickness=0,
        focuscolor="none",
        relief="flat")

    style.map(
        "Eye.Toolbutton",
        background=[("pressed", "#ffffff"), ("active", "#ffffff")],
        foreground=[("pressed", "#1e3d59"), ("active", "#279ef9")]
    )