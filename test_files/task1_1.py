import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def func(x):
    """Функция, которую можно переопределить через ввод пользователя."""
    return np.power(2, -x) - np.sin(x)


def separate_roots():
    try:
        f_str = entry_func.get().strip()
        f = lambda x: eval(f_str,
                           {'np': np, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'log': np.log, 'power': np.power,
                            'x': x})

        a = float(entry_a.get())
        b = float(entry_b.get())
        step = float(entry_step.get())

        x_vals = np.arange(a, b + step, step)
        y_vals = [f(x) for x in x_vals]
        interval_count = 0
        roots_intervals = []
        for i in range(len(y_vals) - 1):
            if y_vals[i] * y_vals[i + 1] < 0:
                roots_intervals.append((x_vals[i], x_vals[i + 1]))
                interval_count += 1


        # fig, ax = plt.subplots()
        # ax.plot(x_vals, y_vals, label=f"f(x) = {f_str}", color='blue')
        # ax.axhline(0, color='red', linestyle='--', alpha=0.5)
        # ax.grid()
        # ax.legend()

        label_result.config(text="Количество отрезков перемены знака: " + str(interval_count) +'\n'+
                                 "Интервалы корней: " + ", ".join([f"[{a:.3f}, {b:.3f}]" for a, b in roots_intervals]))

        # Очистка предыдущего графика

        # if hasattr(separate_roots, 'canvas'):
        #     separate_roots.canvas.get_tk_widget().destroy()
        # separate_roots.canvas = FigureCanvasTkAgg(fig, master=root)
        # separate_roots.canvas.draw()
        # separate_roots.canvas.get_tk_widget().grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Сохраняем интервалы и функцию для уточнения
        separate_roots.intervals = roots_intervals
        separate_roots.f = f

    except Exception as e:
        messagebox.showerror("Ошибка", f"Проверьте ввод:\n{e}")


def refine_root():
    if not hasattr(separate_roots, 'intervals'):
        messagebox.showwarning("Ошибка", "Сначала отделите корни!")
        return

    try:
        epsilon = float(entry_epsilon.get())
        method = combo_method.get()
        intervals = separate_roots.intervals

        f_str = entry_func.get().strip()
        f = lambda x: eval(f_str,
                           {'np': np, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'log': np.log, 'power': np.power,
                            'x': x})

        refined_roots = []
        for a, b in intervals:
            if method == "Метод бисекции":
                refined_roots.append(bisection_method(f, a, b, epsilon))
            elif method == "Метод Ньютона":
                refined_roots.append(newton_method(f, a, b, epsilon))
            elif method == "Модифицированный метод Ньютона":
                refined_roots.append(modified_newton_method(f, a, b, epsilon))
            elif method == "Метод секущих":
                refined_roots.append(secant_method(f, a, b, epsilon))


        label_refined.config(text="Уточненные корни: " + ", ".join([f"{x:.8f}" for x in refined_roots]))

        # fig, ax = plt.subplots()
        # x_vals = np.linspace(float(entry_a.get()), float(entry_b.get()), 1000)
        # y_vals = [f(x) for x in x_vals]
        # ax.plot(x_vals, y_vals, label=f"f(x) = {entry_func.get()}", color='blue')
        # ax.axhline(0, color='red', linestyle='--', alpha=0.5)
        # ax.scatter(refined_roots, [0] * len(refined_roots), color='green', label=f"Корни ({method}, ε={epsilon})")
        # ax.grid()
        # ax.legend()

        # if hasattr(refine_root, 'canvas'): # есть ли у refine_root атрибут canvas?
        #     refine_root.canvas.get_tk_widget().destroy()
        # refine_root.canvas = FigureCanvasTkAgg(fig, master=root)
        # refine_root.canvas.draw()
        # refine_root.canvas.get_tk_widget().grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Проверьте ввод:\n{e}")


# Реализации методов
def bisection_method(f, a, b, epsilon):
    while (b - a) > epsilon:
        c = (a + b) / 2
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2


def newton_method(f, a, b, epsilon):
    df = lambda x: (f(x + epsilon) - f(x)) / epsilon  # Численная производная
    x0 = (a + b) / 2
    while True:
        x1 = x0 - f(x0) / df(x0)
        if abs(x1 - x0) < epsilon:
            return x1
        x0 = x1


def modified_newton_method(f, a, b, epsilon):
    df = lambda x: (f(x + epsilon) - f(x)) / epsilon
    x0 = (a + b) / 2
    df_x0 = df(x0)
    while True:
        x1 = x0 - f(x0) / df_x0
        if abs(x1 - x0) < epsilon:
            return x1
        x0 = x1


def secant_method(f, a, b, epsilon):
    x0, x1 = a, b
    while abs(x1 - x0) > epsilon:
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0, x1 = x1, x2
    return x1


# Настройка GUI
root = tk.Tk()
root.title("Поиск корней")

# Поля ввода
tk.Label(root, text="Функция f(x):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_func = tk.Entry(root, width=30)
entry_func.insert(0, "np.power(2, -x) - np.sin(x)")
entry_func.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Начало интервала (a):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_a = tk.Entry(root)
entry_a.insert(0, "-5")
entry_a.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Конец интервала (b):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_b = tk.Entry(root)
entry_b.insert(0, "10")
entry_b.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Шаг (step):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_step = tk.Entry(root)
entry_step.insert(0, "1e-3")
entry_step.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Точность (ε):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_epsilon = tk.Entry(root)
entry_epsilon.insert(0, "1e-6")
entry_epsilon.grid(row=4, column=1, padx=5, pady=5)

# Выбор метода
tk.Label(root, text="Метод уточнения:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
combo_method = ttk.Combobox(root, values=[
    "Метод бисекции",
    "Метод Ньютона",
    "Модифицированный метод Ньютона",
    "Метод секущих"
])
combo_method.set("Метод бисекции")
combo_method.grid(row=5, column=1, padx=5, pady=5)


tk.Button(root, text="Отделить корни", command=separate_roots).grid(row=6, column=0, pady=10)
tk.Button(root, text="Уточнить корни", command=refine_root).grid(row=6, column=1, pady=10)


label_result = tk.Label(root, text="", justify="left")
label_result.grid(row=7, column=0, columnspan=2)

label_refined = tk.Label(root, text="", justify="left")
label_refined.grid(row=9, column=0, columnspan=2)

root.mainloop()