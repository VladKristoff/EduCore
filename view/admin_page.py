import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

import psycopg2

from database.db_manager import db_manager


class AdminPage:
    def __init__(self, main_frame, app):
        self.main_frame = main_frame
        self.app = app

        self.courses_map = {}
        self.teachers_map = {}

        self.create_widgets()

    def create_widgets(self):
        self.page_container = ttk.Frame(self.main_frame, style="TabMenu.TFrame")
        self.page_container.pack(expand=True, fill="both")

        self.tab_bar = ttk.Frame(self.page_container, style="TabMenu.TFrame")
        self.tab_bar.pack(fill="x", side="top", padx=10, pady=(10, 0))

        self.btn_manager = ttk.Button(
            self.tab_bar,
            text="Аналитика",
            style="ActiveTabButton.TButton",
            command=lambda: self.switch_tab("manager")
        )
        self.btn_manager.pack(side="left")

        self.btn_deans = ttk.Button(
            self.tab_bar,
            text="Расписание",
            style="TabButton.TButton",
            command=lambda: self.switch_tab("deans")
        )
        self.btn_deans.pack(side="left", padx=5)

        exit_btn = ttk.Button(self.tab_bar, text="Выйти",
                              style="ActiveTabButton.TButton",
                              command=lambda: self.app.show_window("login_page"))
        exit_btn.pack(side="right", pady=5)

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
            text="Мониторинг и аналитика курсов",
            style="BlueLabel.TLabel",
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

        table_container = ttk.Frame(self.content_frame, style="AdminMain.TFrame")
        table_container.pack(expand=True, fill="both", padx=20, pady=5)

        columns = ("course_name", "total_hours", "total_cost")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("course_name", text="Учебный курс / Дисциплина")
        self.tree.heading("total_hours", text="Общее кол-во часов")
        self.tree.heading("total_cost", text="Суммарная стоимость затрат")

        self.tree.column("course_name", width=350, anchor="w")
        self.tree.column("total_hours", width=130, anchor="center")
        self.tree.column("total_cost", width=180, anchor="e")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        summary_panel = tk.LabelFrame(
            self.content_frame,
            text=" Итоговые показатели по учебному центру ",
            font=("Arial", 10, "bold"),
            bg="#f8fafc",
            fg="#1e293b",
            bd=1,
            relief="solid",
            padx=15,
            pady=15
        )
        summary_panel.pack(fill="x", padx=20, pady=20)

        self.lbl_total_hours = tk.Label(
            summary_panel,
            text="Всего проведено: 0 академических часов",
            font=("Arial", 11),
            bg="#f8fafc",
            fg="#334155"
        )
        self.lbl_total_hours.pack(side="left", padx=10)

        self.lbl_total_cost = tk.Label(
            summary_panel,
            text="Общие затраты: 0.00 руб.",
            font=("Arial", 11, "bold"),
            bg="#f8fafc",
            fg="#b91c1c"
        )
        self.lbl_total_cost.pack(side="right", padx=10)

        self.load_manager_analytics()

    def load_manager_analytics(self):
        conn = db_manager.connect_bd()
        if not conn:
            print("Ошибка подключения базы данных")
            return
        try:
            cursor = conn.cursor()

            query = """
                        SELECT 
                            c.course_name,
                            SUM(l.actual_duration_hours) AS total_hours,
                            SUM(l.total_cost) AS total_cost
                        FROM lessons l
                        JOIN courses c ON l.course_code = c.course_code
                        GROUP BY c.course_name
                        ORDER BY course_name;
                    """
            cursor.execute(query)
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            grand_total_hours = 0
            grand_total_cost = 0

            for row in rows:
                course, hours, cost = row
                hours = hours if hours else 0
                cost = cost if cost else 0

                self.tree.insert("", "end", values=(
                    course,
                    f"{hours} ч.",
                    f"{cost:,.2f} руб."
                ))

                grand_total_hours += hours
                grand_total_cost += cost

            self.lbl_total_hours.config(text=f"Всего проведено: {grand_total_hours} академических часов")
            self.lbl_total_cost.config(text=f"Общие затраты: {grand_total_cost:,.2f} руб.")

        except Exception as e:
            messagebox.showerror("Ошибка СУБД", f"Не удалось сформировать аналитический отчет:\n{e}")
        finally:
            conn.close()

    def show_deans_content(self):
        student_frame = tk.LabelFrame(
            self.content_frame,
            text=" Управление договорами (Процедура suspend_student_contract) ",
            font=("Arial", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1, relief="solid", padx=15, pady=15
        )
        student_frame.pack(fill="x", padx=20, pady=(20, 10))

        lbl_contract = tk.Label(student_frame, text="Номер договора студента:", font=("Arial", 10), bg="#ffffff",
                                fg="#334155")
        lbl_contract.grid(row=0, column=0, sticky="w", pady=5)

        self.entry_contract = ttk.Entry(student_frame, width=25)
        self.entry_contract.grid(row=0, column=1, padx=10, pady=5)

        btn_suspend = ttk.Button(
            student_frame,
            text="Приостановить договор (Академ)",
            command=self.run_suspend_student_contract
        )
        btn_suspend.grid(row=0, column=2, padx=10, pady=5)

        schedule_frame = tk.LabelFrame(
            self.content_frame,
            text=" Назначение группы на занятие (Перехват исключений бизнеса) ",
            font=("Arial", 10, "bold"), bg="#ffffff", fg="#0f172a", bd=1, relief="solid", padx=15, pady=15
        )
        schedule_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Выбор курса
        lbl_course = tk.Label(schedule_frame, text="Учебный курс / Дисциплина:", font=("Arial", 10), bg="#ffffff",
                              fg="#334155")
        lbl_course.grid(row=0, column=0, sticky="w", pady=8)

        self.combo_course = ttk.Combobox(schedule_frame, width=45, state="readonly")
        self.combo_course.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # Выбор преподавателя
        lbl_teacher = tk.Label(schedule_frame, text="Преподаватель центра:", font=("Arial", 10), bg="#ffffff",
                               fg="#334155")
        lbl_teacher.grid(row=1, column=0, sticky="w", pady=8)

        self.combo_teacher = ttk.Combobox(schedule_frame, width=45, state="readonly")
        self.combo_teacher.grid(row=1, column=1, padx=10, pady=8, sticky="w")

        # Поле ввода даты
        lbl_date = tk.Label(schedule_frame, text="Дата проведения (ГГГГ-ММ-ДД):", font=("Arial", 10), bg="#ffffff",
                            fg="#334155")
        lbl_date.grid(row=2, column=0, sticky="w", pady=8)

        self.entry_date = DateEntry(schedule_frame, width=45,
                                    background='darkblue',
                                    foreground='white',
                                    borderwidth=2,
                                    date_pattern='yyyy-mm-dd')
        self.entry_date.set_date("2026-06-15")
        self.entry_date.grid(row=2, column=1, padx=10, pady=8, sticky="w")

        # Кнопка добавления записи в БД
        btn_add_lesson = ttk.Button(
            schedule_frame,
            text="Добавить занятие в расписание",
            style="SmallBlueButton.TButton",
            command=self.add_lesson_to_schedule
        )
        btn_add_lesson.grid(row=4, column=0, columnspan=2, pady=25)

        self.load_deans_data()

    def load_deans_data(self):
        conn = db_manager.connect_bd()
        if not conn:
            return
        try:
            cursor = conn.cursor()

            # Загружаем курсы
            cursor.execute("SELECT course_code, course_name FROM courses ORDER BY course_name;")
            courses = cursor.fetchall()
            self.combo_course['values'] = [c[1] for c in courses]
            self.courses_map = {c[1]: c[0] for c in courses}  # Карта Название -> Код

            # Загружаем преподавателей
            cursor.execute("SELECT teacher_id, full_name FROM teachers ORDER BY full_name;")
            teachers = cursor.fetchall()
            self.combo_teacher['values'] = [t[1] for t in teachers]
            self.teachers_map = {t[1]: t[0] for t in teachers}  # Карта ФИО -> ID

        except Exception as e:
            messagebox.showerror("Ошибка загрузки списков", f"Не удалось обновить справочники: {e}")
        finally:
            conn.close()

    def run_suspend_student_contract(self):
        contract_num = self.entry_contract.get().strip()
        if not contract_num:
            messagebox.showwarning("Внимание", "Поле номера договора не должно быть пустым!")
            return

        conn = db_manager.connect_bd()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("CALL suspend_student_contract(%s);", (contract_num,))
            conn.commit()

            messagebox.showinfo("Успех", f"Договор №{contract_num} успешно переведен в академический отпуск!")
            self.entry_contract.delete(0, tk.END)

        except psycopg2.Error as e:
            conn.rollback()
            err_msg = e.diag.message_primary if e.diag.message_primary else str(e)
            messagebox.showerror("Ошибка бизнеса", f"Действие отклонено СУБД:\n{err_msg}")
        finally:
            conn.close()

    def add_lesson_to_schedule(self):
        course_name = self.combo_course.get()
        teacher_name = self.combo_teacher.get()
        date_val = self.entry_date.get().strip()

        if not (course_name and teacher_name and date_val):
            messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля формы!")
            return

        course_code = self.courses_map[course_name]
        teacher_id = self.teachers_map[teacher_name]

        conn = db_manager.connect_bd()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO lessons (teacher_id, course_code, lesson_date) 
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (teacher_id, course_code, date_val))
            conn.commit()
            messagebox.showinfo("Успех", "Занятие успешно внесено в расписание учебного центра!")

        except psycopg2.Error as e:
            conn.rollback()
            err_msg = str(e).lower()
            # Сценарий на случай, если триггер/процедура на стороне БД всё-таки будут созданы
            if "отпуск" in err_msg or "отстранен" in err_msg:
                messagebox.showerror(
                    "Предупреждение",
                    "Ошибка: Данный преподаватель временно недоступен для ведения занятий!"
                )
            else:
                messagebox.showerror("Ошибка БД", f"Не удалось добавить запись в расписание:\n{e}")
        finally:
            conn.close()