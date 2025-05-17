import customtkinter as ctk
# import customtkinter as messagebox
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.custom_m_box import CTkMessageBox


class InterpolationTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.table_data = []
        self.sorted = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.func_label = ctk.CTkLabel(self, text="Функция f(x):")
        self.func_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.func_entry = ctk.CTkEntry(self, width=400)
        self.func_entry.insert(0, "log(1 + x)")
        self.func_entry.grid(row=1, column=0, padx=10, sticky="ew")

        params_frame = ctk.CTkFrame(self)
        params_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # def number_check(event=None, value='12'):
        #     try:
        #         entry = int(value)
        #     except ValueError:
        #         CTkMessageBox(self, "Warning",
        #                       f"Введено не допустимое значение {value}")

        def on_n_change(event=None):
            try:
                m = int(self.m_entry.get())  # текущее m + 1
                n_text = self.n_entry.get()  # текущий текст в поле n

                if not n_text:  # Если поле пустое, ничего не делаем
                    return

                n = int(n_text)  # Пытаемся преобразовать в число

                if n <= m - 1:
                    self.n_entry.configure(border_color="#565b5e")  # Нормальный цвет

                else:  # Если n > m, исправляем на m-1
                    self.n_entry.delete(0, "end")
                    self.n_entry.insert(0, str(m - 1))
                    self.n_entry.configure(border_color="red")  # Подсветка ошибки
                    #messagebox.showerror("Warning", f"Введено не допустимое значение n. Допустимые значения для n: n <= m")
                    CTkMessageBox(self, "Warning",
                                  f"Введено не допустимое значение n. Допустимые значения для n: n <= m")

            except ValueError:
                self.n_entry.configure(border_color="red")  # Если введено не число

        def on_m_change(event=None):
            try:
                m = int(self.m_entry.get())  # текущее m
                n = int(self.n_entry.get())  # текущee n

                if n > m - 1:  # Если n >= m, исправляем на m-1
                    self.m_entry.delete(0, "end")
                    self.m_entry.insert(0, str(n + 1))
                    self.m_entry.configure(border_color="red")  # Подсветка ошибки
                    #messagebox.showerror("Warning", f"Введено не допустимое значение m. Допустимые значения для n: n <= m")
                    CTkMessageBox(self, "Warning",
                                  f"Введено не допустимое значение n. Допустимые значения для n: n <= m")
                else:
                    self.m_entry.configure(border_color="#565b5e")  # Нормальный цвет
            except ValueError:
                self.m_entry.configure(border_color="red")  # Если введено не число

        ctk.CTkLabel(params_frame, text="Количество значений в таблице (m+1):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.m_entry = ctk.CTkEntry(params_frame, width=100)
        self.m_entry.insert(0, "16")
        self.m_entry.grid(row=0, column=1, padx=5, pady=5)

        # self.m_entry.bind("<KeyRelease>", on_m_change)
        self.m_entry.bind("<Return>", on_m_change)  # Проверка по Enter
        self.m_entry.bind("<FocusOut>", on_m_change)  # Проверка при потере фокуса

        ctk.CTkLabel(params_frame, text="a:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.a_entry = ctk.CTkEntry(params_frame, width=100)
        self.a_entry.insert(0, "0")
        self.a_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(params_frame, text="b:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.b_entry = ctk.CTkEntry(params_frame, width=100)
        self.b_entry.insert(0, "1.5")
        self.b_entry.grid(row=0, column=5, padx=5, pady=5)

        ctk.CTkLabel(params_frame, text="Точка интерполирования x:").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.x_entry = ctk.CTkEntry(params_frame, width=100)
        self.x_entry.insert(0, "0")
        self.x_entry.grid(row=0, column=7, padx=5, pady=5)

        ctk.CTkLabel(params_frame, text="Степень многочлена (n):").grid(row=0, column=8, padx=5, pady=5, sticky="e")
        self.n_entry = ctk.CTkEntry(params_frame, width=100)
        self.n_entry.insert(0, "8")
        self.n_entry.grid(row=0, column=9, padx=5, pady=5)

        #self.n_entry.bind("<KeyRelease>", on_n_change)
        self.n_entry.bind("<Return>", on_n_change)  # Проверка по Enter
        self.n_entry.bind("<FocusOut>", on_n_change)  # Проверка при потере фокуса



        self.table_method_label = ctk.CTkLabel(self, text="Метод:")
        self.table_method_label.grid(row=3, column=0, padx=10, sticky="w")

        self.table_method_combo = ctk.CTkComboBox(self, values=[
            "Равноотстоящие",
            "Случайные"
        ])

        self.table_method_combo.set("Равноотстоящие")
        self.table_method_combo.grid(row=4, column=0, padx=10, sticky="w")



        self.method_label = ctk.CTkLabel(self, text="Метод интерполирования:")
        self.method_label.grid(row=5, column=0, padx=10, sticky="w")

        self.method_combo = ctk.CTkComboBox(self, values=[
            "Метод Ньютона",
            "Метод Лагранжа"
        ])

        self.method_combo.set("Метод Ньютона")
        self.method_combo.grid(row=6, column=0, padx=10, sticky="w")


        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.create_table_button = ctk.CTkButton(
            buttons_frame,
            text="Создать таблицу",
            command=self.create_table
        )
        self.create_table_button.pack(side="left", padx=5)

        self.create_table_button = ctk.CTkButton(
            buttons_frame,
            text="Отсортировать таблицу",
            command=self.sort_table
        )
        self.create_table_button.pack(side="left", padx=5)

        self.interpolate_button = ctk.CTkButton(
            buttons_frame,
            text="Интерполировать",
            command=self.interpolate
        )
        self.interpolate_button.pack(side="left", padx=5)

        self.result_label = ctk.CTkLabel(self, text="Результат:", anchor="w", justify="left")
        self.result_label.grid(row=8, column=0, padx=10, sticky="nw")

        self.er_label = ctk.CTkLabel(self, text="Абсолютная погрешность:", anchor="w", justify="left")
        self.er_label.grid(row=9, column=0, padx=10, sticky="nw")

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=10, column=0, padx=10, sticky="nw")

        self.table = ctk.CTkScrollableFrame(table_frame, width=800, height=400)
        self.table.pack(side="left", padx=5, pady=5)


    def create_table(self):
        try:
            m = int(self.m_entry.get())
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            x = float(self.x_entry.get())

            f_str = self.func_entry.get().strip()
            f = lambda x: eval(f_str, {
                'np': np, 'sin': np.sin, 'cos': np.cos,
                'exp': np.exp, 'log': np.log, 'power': np.power, 'x': x
            })

            method = self.table_method_combo.get()

            if method == "Равноотстоящие":
                x_values = np.linspace(a, b, m + 1)
                self.sorted = False
            else:
                x_values = np.random.uniform(a, b, m + 1)
                self.sorted = False

            dist_x = []
            for i in range(len(x_values)):
                dist_x.append(x - x_values[i])

                # Примерная функция (замените на свою)
            f_values = f(x_values)

            self.table_data = list(zip(x_values, f_values, dist_x))
            self.display_table()

        except Exception as e:
            CTkMessageBox(self, "Error",
                          f"Ошибка: {str(e)}")
            #self.show_error(f"Ошибка: {str(e)}")

    def display_table(self):
        # Очищаем предыдущую таблицу
        for widget in self.table.winfo_children():
            widget.destroy()

        n = int(self.n_entry.get())

        # Заголовки
        ctk.CTkLabel(self.table, text="Номер узла").grid(row=0, column=0, padx=5, pady=2)
        ctk.CTkLabel(self.table, text="x_k").grid(row=0, column=1, padx=5, pady=2)
        ctk.CTkLabel(self.table, text="f(x_k)").grid(row=0, column=2, padx=5, pady=2)
        ctk.CTkLabel(self.table, text="Расстояние до х").grid(row=0, column=3, padx=5)

        if self.sorted:
            data = self.table_data
            selected_nodes = data[:n + 1]

            selected_color = "#4fc3f7"  # Голубой текст выделенных ячеек
            unselected_color = "#34495e"  # Темно-синий

            for i, (x, fx, dist_x) in enumerate(data, start=1):
                is_selected = (x, fx, dist_x) in selected_nodes
                text_color = selected_color if is_selected else unselected_color

                ctk.CTkLabel(self.table, text=f"{i}").grid(row=i, column=0, padx=5, pady=2)
                ctk.CTkLabel(self.table, text=f"{x:.4f}", text_color=text_color).grid(row=i, column=1, padx=5, pady=2)
                ctk.CTkLabel(self.table, text=f"{fx:.4f}", text_color=text_color).grid(row=i, column=2, padx=5, pady=2)
                ctk.CTkLabel(self.table, text=f"{dist_x:.4f}", text_color=text_color).grid(row=i, column=3, padx=5, pady=2)
        else:
            for i, (x, fx, dist_x) in enumerate(self.table_data, start=1):
                ctk.CTkLabel(self.table, text=f"{i}").grid(row=i, column=0, padx=5, pady=2)
                ctk.CTkLabel(self.table, text=f"{x:.4f}").grid(row=i, column=1, padx=5, pady=2)
                ctk.CTkLabel(self.table, text=f"{fx:.4f}").grid(row=i, column=2, padx=5, pady=2)
                ctk.CTkLabel(self.table, text=f"{dist_x:.4f}").grid(row=i, column=3, padx=5, pady=2)

    def sort_table(self):
        try:

            x = float(self.x_entry.get())
            n = int(self.n_entry.get())
            m = len(self.table_data) - 1

            if n > m:
                raise ValueError(f"Степень n ({n}) должна быть ≤ m ({m})")

            # Сортировка по расстоянию до x
            sorted_data = sorted(self.table_data, key=lambda item: abs(item[0] - x))
            x_sorted = [item[0] for item in sorted_data]
            f_sorted = [item[1] for item in sorted_data]

            dist_x = []
            for i in range(len(x_sorted)):
                dist_x.append(x - x_sorted[i])


            self.sorted = True
            self.table_data = list(zip(x_sorted, f_sorted, dist_x))
            self.display_table()



        except Exception as e:
            CTkMessageBox(self, "Error",
                          f"Ошибка: {str(e)}")

    def interpolate(self):
        try:
            if not self.table_data:
                #raise ValueError("Сначала создайте таблицу значений")
                CTkMessageBox(self, "Error",
                              f"Сначала создайте таблицу значений")
                return None

            flag_sorted = self.sorted

            if flag_sorted == False:
                CTkMessageBox(self, "Error",
                              f"Сначала отсортируйте таблицу значений")
                return None

            x = float(self.x_entry.get())
            n = int(self.n_entry.get())
            m = len(self.table_data) - 1

            if n > m:
                raise ValueError(f"Степень n ({n}) должна быть ≤ m ({m})")

            data = self.table_data

            selected_nodes = data[:n + 1]

            x_sorted = [item[0] for item in data]
            f_sorted = [item[1] for item in data]

            # Выбираем n+1 ближайших узлов
            x_nodes = x_sorted[:n + 1]
            f_nodes = f_sorted[:n + 1]

            method = self.method_combo.get()

            interpolation_result = 0
            abs_err = 0

            # Интерполяция Лагранжа
            if method == "Метод Лагранжа":
                interpolation_result, abs_err = self.lagrange_interpolation(self, x, x_nodes, f_nodes)

            # Интерполяция Ньютона
            if method == "Метод Ньютона":
                interpolation_result, abs_err = self.newton_interpolation(self, x, x_nodes, f_nodes)

            self.result_label.configure(text=f"Значение в точке х ({method}): {interpolation_result}")
            self.er_label.configure(text=f"Абсолютная погрешность ({method}): {abs_err}")

            # # Визуализация
            # self.plot_results(x, x_nodes, f_nodes, lagrange_result)

        except Exception as e:
            CTkMessageBox(self, "Error",
                          f"Ошибка: {str(e)}")
            #self.show_error(f"Ошибка: {str(e)}")

    @staticmethod
    def lagrange_interpolation(self, x, x_nodes, f_nodes):
        result = 0.0
        n = len(x_nodes)

        f_str = self.func_entry.get().strip()
        f = lambda x: eval(f_str, {
            'np': np, 'sin': np.sin, 'cos': np.cos,
            'exp': np.exp, 'log': np.log, 'power': np.power, 'x': x
        })

        for i in range(n):
            term = f_nodes[i]
            for j in range(n):
                if i != j:
                    term *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
            result += term

        # Контроль: сумма коэффициентов должна быть 1
        sum_coeff = 0.0
        for i in range(n):
            coeff = 1.0
            for j in range(n):
                if i != j:
                    coeff *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
            sum_coeff += coeff

        print(f"Контроль Лагранжа (сумма коэффициентов): {sum_coeff:.10f}")

        err = abs(f(x) - result)

        return result, err

    @staticmethod
    def newton_interpolation(self, x, x_nodes, f_nodes):
        n = len(x_nodes)

        f_str = self.func_entry.get().strip()
        f = lambda x: eval(f_str, {
            'np': np, 'sin': np.sin, 'cos': np.cos,
            'exp': np.exp, 'log': np.log, 'power': np.power, 'x': x
        })

        # Таблица разделенных разностей
        table = [[0.0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            table[i][0] = f_nodes[i]

        for j in range(1, n):
            for i in range(n - j):
                table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x_nodes[i + j] - x_nodes[i])

        # Интерполяция
        result = table[0][0]
        product = 1.0

        for i in range(1, n):
            product *= (x - x_nodes[i - 1])
            result += table[0][i] * product

        err = abs(f(x) - result)

        return result, err

    def update_content(self):
        """Метод для обновления содержимого при переключении на эту вкладку"""
        print("Обновление вкладки Интерполяция")