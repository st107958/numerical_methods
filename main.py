import customtkinter as ctk
from modules.task1 import RootFindingTab
from modules.task2 import InterpolationTab

# Импортируйте другие модули по мере их создания

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NumericalMethodsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Методы вычислений")
        self.geometry("1200x800")
        self.create_widgets()

    def create_widgets(self):
        # Создаем Notebook (вкладки)
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True)

        # Добавляем вкладки
        self.notebook.add("Нахождение корней")
        self.notebook.add("Алгебраическое интерполирование")
        # Добавьте другие вкладки по мере необходимости

        # Создаем содержимое вкладок
        self.root_finding_tab = RootFindingTab(self.notebook.tab("Нахождение корней"))
        self.root_finding_tab.pack(fill="both", expand=True)

        # Здесь можно добавить другие модули
        self.interpolation_tab = InterpolationTab(self.notebook.tab("Алгебраическое интерполирование"))
        self.interpolation_tab.pack(fill="both", expand=True)

        # Подписываемся на изменение вкладки (специальный метод для CTkTabview)
        self.notebook.configure(command=self.on_tab_change)

    def on_tab_change(self):
        """Обновляем содержимое активной вкладки"""
        selected_tab = self.notebook.get()

        if selected_tab == "Нахождение корней":
            self.root_finding_tab.update_content()
        elif selected_tab == "Интерполирование":
            self.interpolation_tab.update_content()


if __name__ == "__main__":
    app = NumericalMethodsApp()
    app.mainloop()