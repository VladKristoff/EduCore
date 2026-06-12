import tkinter as tk
from tkinter import *
from tkinter import ttk

class AdminPage:
    def __init__(self, main_frame, app):
        self.main_frame = main_frame
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        self.page_container = ttk.Frame(self.main_frame, style="TabMenu.TFrame")
        self.page_container.pack(expand=True, fill="both")

        self.tab_bar = ttk.Frame(self.page_container, style="TabMenu.TFrame")
        self.tab_bar.pack(fill="x", side="top", padx=10, pady=(10, 0))

        self.btn_manager = ttk.Button(
            self.tab_bar,
            text="Аналитика (Руководитель)",
            style="ActiveTabButton.TButton",
            command=lambda: self.switch_tab("manager")
        )
        self.btn_manager.pack(side="left")

        self.btn_deans = ttk.Button(
            self.tab_bar,
            text="Расписание (Деканат)",
            style="TabButton.TButton",
            command=lambda: self.switch_tab("deans")
        )
        self.btn_deans.pack(side="left", padx=5)

        separator = ttk.Frame(self.page_container, height=2, style="AdminMain.TFrame")
        separator.pack(fill="x", padx=10)

        self.content_frame = ttk.Frame(self.page_container, style="AdminMain.TFrame")
        self.content_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        self.show_manager_content()

    def switch_tab(self, tab_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.btn_manager.configure(style="TabButton.TButton")
        self.btn_deans.configure(style="TabButton.TButton")

        if tab_name == "manager":
            self.btn_manager.configure(style="ActiveTabButton.TButton")
            self.show_manager_content()
        elif tab_name == "deans":
            self.btn_deans.configure(style="ActiveTabButton.TButton")
            self.show_deans_content()

    def show_manager_content(self):
        title = ttk.Label(
            self.content_frame,
            text="Мониторинг и Аналитика Курсов",
            font=("Arial", 16, "bold"),
            background="#ffffff",
            foreground="#0f172a"
        )
        title.pack(anchor="w", padx=20, pady=20)

        placeholder = ttk.Label(
            self.content_frame,
            text="[Здесь будет Treeview отчет: Курсы | Часы | Затраты]",
            font=("Arial", 11), background="#ffffff", foreground="#64748b"
        )
        placeholder.pack(pady=50)

    def show_deans_content(self):
        title = ttk.Label(
            self.content_frame,
            text="Управление Расписанием Занятий",
            font=("Arial", 16, "bold"),
            background="#ffffff",
            foreground="#0f172a"
        )
        title.pack(anchor="w", padx=20, pady=20)

        placeholder = ttk.Label(
            self.content_frame,
            text="[Здесь будут поля добавления занятий и обработка ошибок отпусков]",
            font=("Arial", 11), background="#ffffff", foreground="#64748b"
        )
        placeholder.pack(pady=50)
