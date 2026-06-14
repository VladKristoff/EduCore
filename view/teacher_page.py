import tkinter as tk
from datetime import datetime, time, timedelta
from tkinter import *
from tkinter import ttk, messagebox

from database.db_manager import db_manager


class TeacherPage:
    def __init__(self, main_frame, app):
        self.main_frame = main_frame
        self.app = app

        # Переменные для управления таймером
        self.timer_running = False
        self.seconds_passed = 0
        self.timer_after_id = None
        self.current_lesson_id = None

        self.create_widgets()

    def create_widgets(self):
        self.page_container = ttk.Frame(self.main_frame, style="TabMenu.TFrame")
        self.page_container.pack(expand=True, fill="both")

        self.tab_bar = ttk.Frame(self.page_container, style="TabMenu.TFrame")
        self.tab_bar.pack(fill="x", side="top", padx=10, pady=(10, 0))

        self.btn_start_lesson = ttk.Button(
            self.tab_bar,
            text="Начать занятие",
            style="ActiveTabButton.TButton",
            state="disabled",
            command=lambda : self.start_lesson()
        )
        self.btn_start_lesson.pack(side="left")

        self.btn_stop_lesson = ttk.Button(
            self.tab_bar,
            text="Завершить занятие",
            style="TabButton.TButton",
            state="disabled",
            command=lambda : self.stop_lesson()
        )
        self.btn_stop_lesson.pack(side="left", padx=5)

        self.timer_label = ttk.Label(self.tab_bar, text="00:00", style="TimerLabel.TLabel")
        self.timer_label.pack(side="left", padx=20)

        exit_btn = ttk.Button(self.tab_bar, text="Выйти",
                              style="ActiveTabButton.TButton",
                              command=lambda: self.on_exit())
        exit_btn.pack(side="right", pady=5)

        self.content_frame = ttk.Frame(self.page_container, style="AdminMain.TFrame")
        self.content_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        # Таблица
        columns = ("lesson_id", "course_code", "lesson_date", "start_time", "end_time", "duration", "total_cost", "status")

        self.tree = ttk.Treeview(self.content_frame, columns=columns,
                                 show="headings",
                                 selectmode="browse",
                                 style="Treeview")

        self.tree.heading("lesson_id", text="ID")
        self.tree.heading("course_code", text="Код курса")
        self.tree.heading("lesson_date", text="Дата")
        self.tree.heading("start_time", text="Время начала")
        self.tree.heading("end_time", text="Время окончания")
        self.tree.heading("duration", text="Акад. часы")
        self.tree.heading("total_cost", text="Стоимость")
        self.tree.heading("status", text="Статус")

        self.tree.column("lesson_id", width=50, anchor="center")
        self.tree.column("course_code", width=100, anchor="center")
        self.tree.column("lesson_date", width=100, anchor="center")
        self.tree.column("start_time", width=100, anchor="center")
        self.tree.column("end_time", width=110, anchor="center")
        self.tree.column("duration", width=90, anchor="center")
        self.tree.column("total_cost", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_lesson_select)

        self.tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        self.load_lessons_data()

    def load_lessons_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = db_manager.connect_bd()
            with conn.cursor() as cursor:
                query = """
                            SELECT lesson_id, course_code, lesson_date, start_time, end_time, 
                                   actual_duration_hours, total_cost, status 
                            FROM lessons 
                            ORDER BY lesson_date DESC, start_time DESC;
                        """
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    lesson_id, course_code, l_date, s_time, e_time, duration, cost, status = row

                    formatted_date = l_date.strftime('%Y-%m-%d') if l_date else ""
                    formatted_start = s_time.strftime('%H:%M') if s_time else ""
                    formatted_end = e_time.strftime('%H:%M') if e_time else ""

                    formatted_duration = duration if duration is not None else "—"
                    formatted_cost = f"{cost} руб." if cost is not None else "—"

                    self.tree.insert("", "end", values=(
                        lesson_id,
                        course_code,
                        formatted_date,
                        formatted_start,
                        formatted_end,
                        formatted_duration,
                        formatted_cost,
                        status
                    ))
        except Exception as e:
            messagebox.showerror("Ошибка СУБД", f"Не удалось загрузить журнал занятий:\n{e}")

    def on_lesson_select(self, event):
        # Если занятие прямо сейчас идет, не даем переключать кнопки по кликам
        if self.timer_running:
            return

        selected_item = self.tree.selection()
        if not selected_item:
            self.btn_start_lesson.config(state="disabled")
            return

        item_values = self.tree.item(selected_item, "values")
        status = item_values[7]  # Индекс скрытой колонки статуса

        if status == "planned":
            self.btn_start_lesson.config(state="normal")
        else:
            self.btn_start_lesson.config(state="disabled")

    def start_lesson(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, "values")
        self.current_lesson_id = item_values[0]

        now = datetime.now()
        start_time_str = now.strftime('%H:%M:%S')
        lesson_date_str = now.strftime('%Y-%m-%d')

        try:
            conn = db_manager.connect_bd()
            with conn.cursor() as cursor:
                query = """
                    UPDATE lessons 
                    SET start_time = %s, lesson_date = %s, status = 'active' 
                    WHERE lesson_id = %s
                """
                cursor.execute(query, (start_time_str, lesson_date_str, self.current_lesson_id))
                conn.commit()

            self.tree.config(selectmode="none")
            self.btn_start_lesson.config(state="disabled")
            self.btn_stop_lesson.config(state="normal")

            self.timer_running = True
            self.seconds_passed = 0
            self.update_timer()

            self.load_lessons_data()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось начать занятие в БД:\n{e}")

    def update_timer(self):
        if self.timer_running:
            mins, secs = divmod(self.seconds_passed, 60)
            hours, mins = divmod(mins, 60)

            if hours > 0:
                time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
            else:
                time_str = f"{mins:02d}:{secs:02d}"

            self.timer_label.config(text=time_str)
            self.seconds_passed += 1

            self.timer_after_id = self.main_frame.after(1000, self.update_timer)

    def stop_lesson(self):
        if not self.current_lesson_id:
            return

        self.timer_running = False
        if self.timer_after_id:
            self.main_frame.after_cancel(self.timer_after_id)

        now = datetime.now()

        try:
            conn = db_manager.connect_bd()
            with conn.cursor() as cursor:
                query_get_start = "SELECT start_time FROM lessons WHERE lesson_id = %s"
                cursor.execute(query_get_start, (self.current_lesson_id,))
                result = cursor.fetchone()

                if not result:
                    messagebox.showerror("Ошибка", "Занятие не найдено")
                    return

                start_time = result[0]
                today = datetime.now().date()
                start_datetime = datetime.combine(today, start_time)

                # 1. Считаем реальную длительность в секундах
                real_duration_seconds = (now - start_datetime).total_seconds()

                if real_duration_seconds < 0:
                    messagebox.showerror("Ошибка", "Время окончания раньше времени начала")
                    return

                # ================================================================
                # МОДИФИКАЦИЯ ДЛЯ БЫСТРОЙ ПРОВЕРКИ И ТЕСТИРОВАНИЯ
                # Коэффициент ускорения. 60 означает: 1 реальная секунда = 1 минута в системе
                time_speed_factor = 60

                # Виртуальная длительность в секундах с учетом ускорения
                virtual_duration_seconds = real_duration_seconds * time_speed_factor

                # Рассчитываем виртуальное время окончания занятия для записи в БД
                # (чтобы в таблице была красивая разница во времени, а не 5 секунд)
                virtual_end_datetime = start_datetime + timedelta(seconds=virtual_duration_seconds)
                end_time_str = virtual_end_datetime.strftime('%H:%M:%S')

                # Считаем академические часы по виртуальному времени (1 ак. ч. = 2700 секунд)
                acad_hours = round(virtual_duration_seconds / 2700, 1)
                # ================================================================

                if acad_hours < 0.1:
                    acad_hours = 0.1

                # Ставка (в Модуле 5 она у тебя будет считаться через БД, пока оставляем хардкод для интерфейса)
                hourly_rate = 1500
                total_cost = round(acad_hours * hourly_rate, 2)

                query_update = """
                    UPDATE lessons 
                    SET end_time = %s, actual_duration_hours = %s, total_cost = %s, status = 'completed' 
                    WHERE lesson_id = %s
                """
                cursor.execute(query_update, (end_time_str, acad_hours, total_cost, self.current_lesson_id))
                conn.commit()

            messagebox.showinfo("Успех (Режим тестирования)",
                                f"Занятие завершено!\n"
                                f"Реально прошло: {int(real_duration_seconds)} сек.\n"
                                f"Виртуально прошло: {round(virtual_duration_seconds / 60, 1)} мин.\n"
                                f"Длительность: {acad_hours} ак. ч.\n"
                                f"Стоимость: {total_cost} руб.")

            self.current_lesson_id = None

            self.tree.config(selectmode="browse")
            self.btn_start_lesson.config(state="normal")
            self.btn_stop_lesson.config(state="disabled")

            self.load_lessons_data()

        except Exception as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось завершить занятие: {e}")

    def on_exit(self):
        if self.timer_running:
            if not messagebox.askyesno("Предупреждение",
                                       "У вас идет занятие! Вы уверены, что хотите выйти? Данные текущего урока не сохранятся."):
                return
            self.timer_running = False
            if self.timer_after_id:
                self.main_frame.after_cancel(self.timer_after_id)

        self.app.show_window("login_page")




