import customtkinter as ctk


class CTkMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, type="info"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)

        # Выбор цвета в зависимости от типа
        colors = {
            "info": ("#3b8ed0", "#1f6aa5"),
            "warning": ("#f0ad4e", "#eea236"),
            "error": ("#d9534f", "#d43f3a")
        }
        color, hover_color = colors.get(type, ("#3b8ed0", "#1f6aa5"))

        self.label = ctk.CTkLabel(self, text=message, wraplength=380)
        self.label.pack(pady=30, padx=20)

        self.button = ctk.CTkButton(
            self,
            text="OK",
            fg_color=color,
            hover_color=hover_color,
            command=self.destroy
        )
        self.button.pack(pady=10)

        self.grab_set()  # Модальное окно
