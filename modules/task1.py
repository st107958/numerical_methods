import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RootFindingTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.func_label = ctk.CTkLabel(self, text="Функция f(x):")
        self.func_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.func_entry = ctk.CTkEntry(self, width=400)
        self.func_entry.insert(0, "power(2, -x) - sin(x)")
        self.func_entry.grid(row=1, column=0, padx=10, sticky="ew")

        params_frame = ctk.CTkFrame(self)
        params_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(params_frame, text="a:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.a_entry = ctk.CTkEntry(params_frame, width=100)
        self.a_entry.insert(0, "-5")
        self.a_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(params_frame, text="b:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.b_entry = ctk.CTkEntry(params_frame, width=100)
        self.b_entry.insert(0, "10")
        self.b_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(params_frame, text="N (кол-во шагов):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.step_entry = ctk.CTkEntry(params_frame, width=100)
        self.step_entry.insert(0, "1e4")
        self.step_entry.grid(row=0, column=5, padx=5, pady=5)

        ctk.CTkLabel(params_frame, text="ε (точность):").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.epsilon_entry = ctk.CTkEntry(params_frame, width=100)
        self.epsilon_entry.insert(0, "1e-6")
        self.epsilon_entry.grid(row=0, column=7, padx=5, pady=5)

        self.method_label = ctk.CTkLabel(self, text="Метод уточнения:")
        self.method_label.grid(row=3, column=0, padx=10, sticky="w")

        self.method_combo = ctk.CTkComboBox(self, values=[
            "Метод бисекции",
            "Метод Ньютона",
            "Модифицированный метод Ньютона",
            "Метод секущих"
        ])
        self.method_combo.set("Модифицированный метод Ньютона")
        self.method_combo.grid(row=4, column=0, padx=10, sticky="w")

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.separate_button = ctk.CTkButton(
            buttons_frame,
            text="Отделить корни",
            command=self.separate_roots
        )
        self.separate_button.pack(side="left", padx=5)

        self.refine_button = ctk.CTkButton(
            buttons_frame,
            text="Уточнить корни",
            command=self.refine_root
        )
        self.refine_button.pack(side="left", padx=5)

        self.result_label = ctk.CTkLabel(self, text="", anchor="w", justify="left")
        self.result_label.grid(row=6, column=0, padx=10, sticky="ew")

        self.refined_label = ctk.CTkLabel(self, text="", anchor="w", justify="left")
        self.refined_label.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.figure, self.ax = plt.subplots(figsize=(8, 4))

        self.figure.patch.set_facecolor('#2b2b2b')  # Цвет фона фигуры (как в CustomTkinter)
        self.ax.set_facecolor('#353535')  # Цвет фона области графика
        self.ax.xaxis.label.set_color('#4cc9f0')  # Цвет подписи оси X
        self.ax.yaxis.label.set_color('#4cc9f0')  # Цвет подписи оси Y
        self.ax.title.set_color('#e6e6e6')  # Цвет заголовка
        self.ax.tick_params(colors='#e6e6e6')  # Цвет делений

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=8, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # сохранение для вывода
        self.intervals = []
        self.f = None

    def separate_roots(self):
        try:
            f_str = self.func_entry.get().strip()
            f = lambda x: eval(f_str, {
                'np': np, 'sin': np.sin, 'cos': np.cos,
                'exp': np.exp, 'log': np.log, 'power': np.power, 'x': x
            })

            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            N = float(self.step_entry.get())

            step = (b - a) / N

            x_vals = np.arange(a, b + step, step)
            y_vals = [f(x) for x in x_vals]

            self.ax.clear()
            self.ax.plot(x_vals, y_vals, label=f"f(x) = {f_str}", color='#1f77b4')
            self.ax.grid(True, linestyle='--', alpha=0.7)

            self.figure.patch.set_facecolor('#2b2b2b')  # Цвет фона фигуры (как в CustomTkinter)
            self.ax.set_facecolor('#353535')  # Цвет фона области графика
            self.ax.xaxis.label.set_color('#4cc9f0')  # Цвет подписи оси X
            self.ax.yaxis.label.set_color('#4cc9f0')  # Цвет подписи оси Y
            self.ax.title.set_color('#e6e6e6')  # Цвет заголовка
            self.ax.tick_params(colors='#e6e6e6')  # Цвет делений

            self.ax.legend()
            self.canvas.draw()

            self.intervals = []
            interval_count = 0
            for i in range(len(y_vals) - 1):
                if y_vals[i] * y_vals[i + 1] < 0:
                    self.intervals.append((x_vals[i], x_vals[i + 1]))
                    interval_count += 1

            intervals_text = ", ".join([f"[{a:.3f}, {b:.3f}]" for a, b in self.intervals])
            self.result_label.configure(
                text=f"Количество отрезков перемены знака: {interval_count}\n"
                     f"Интервалы корней: {intervals_text}"
            )

            self.f = f  # сохранила для уточнения корней

        except Exception as e:
            self.result_label.configure(text=f"Ошибка: {str(e)}")

    def refine_root(self):
        if not self.intervals or self.f is None:
            self.refined_label.configure(text="Сначала отделите корни!")
            return

        try:
            epsilon = float(self.epsilon_entry.get())
            method = self.method_combo.get()

            refined_roots = []
            for a, b in self.intervals:
                if method == "Метод бисекции":
                    refined_roots.append(self.bisection_method(self.f, a, b, epsilon))
                elif method == "Метод Ньютона":
                    refined_roots.append(self.newton_method(self.f, a, b, epsilon))
                elif method == "Модифицированный метод Ньютона":
                    refined_roots.append(self.modified_newton_method(self.f, a, b, epsilon))
                elif method == "Метод секущих":
                    refined_roots.append(self.secant_method(self.f, a, b, epsilon))

            a = float(self.a_entry.get())
            b = float(self.b_entry.get())

            x_vals = np.linspace(a, b, 1000)
            y_vals = [self.f(x) for x in x_vals]

            self.ax.clear()
            self.ax.plot(x_vals, y_vals, label=f"f(x) = {self.func_entry.get()}", color='blue')
            self.ax.scatter(
                refined_roots,
                [0] * len(refined_roots),
                color='green',
                label=f"Корни ({method}, ε={epsilon})"
            )
            self.ax.grid(True, linestyle='--', alpha=0.7)

            self.figure.patch.set_facecolor('#2b2b2b')  # Цвет фона фигуры (как в CustomTkinter)
            self.ax.set_facecolor('#353535')  # Цвет фона области графика
            self.ax.xaxis.label.set_color('#4cc9f0')  # Цвет подписи оси X
            self.ax.yaxis.label.set_color('#4cc9f0')  # Цвет подписи оси Y
            self.ax.title.set_color('#e6e6e6')  # Цвет заголовка
            self.ax.tick_params(colors='#e6e6e6')  # Цвет делений

            self.ax.legend()
            self.canvas.draw()

            roots_text = ", ".join([f"{x:.20f}" for x in refined_roots])
            self.refined_label.configure(text=f"Уточненные корни ({method}): {roots_text}")

        except Exception as e:
            self.refined_label.configure(text=f"Ошибка: {str(e)}")

    @staticmethod
    def bisection_method(f, a, b, epsilon):
        while (b - a) > epsilon:
            c = (a + b) / 2
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2

    @staticmethod
    def newton_method(f, a, b, epsilon):
        df = lambda x: (f(x + epsilon) - f(x)) / epsilon
        x0 = (a + b) / 2
        while True:
            x1 = x0 - f(x0) / df(x0)
            if abs(x1 - x0) < epsilon:
                return x1
            x0 = x1

    @staticmethod
    def modified_newton_method(f, a, b, epsilon):
        df = lambda x: (f(x + epsilon) - f(x)) / epsilon
        x0 = (a + b) / 2
        df_x0 = df(x0)
        while True:
            x1 = x0 - f(x0) / df_x0
            if abs(x1 - x0) < epsilon:
                return x1
            x0 = x1

    @staticmethod
    def secant_method(f, a, b, epsilon):
        x0, x1 = a, b
        while abs(x1 - x0) > epsilon:
            x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
            x0, x1 = x1, x2
        return x1

    def update_content(self):
        """Метод для обновления содержимого при переключении на эту вкладку"""
        print("Обновление вкладки Нахождение корней")