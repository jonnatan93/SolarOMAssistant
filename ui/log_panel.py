from datetime import datetime
import customtkinter as ctk


class LogPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="Registro",
            font=("Segoe UI", 15, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.console = ctk.CTkTextbox(
            self,
            height=220
        )

        self.console.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.console.insert(
            "end",
            "Esperando ejecución...\n"
        )

        self.console.configure(
            state="disabled"
        )

    # -----------------------------------------------------

    def clear(self):

        self.console.configure(state="normal")

        self.console.delete(
            "1.0",
            "end"
        )

        self.console.configure(
            state="disabled"
        )

    # -----------------------------------------------------

    def log(self, message):

        hora = datetime.now().strftime("%H:%M:%S")

        self.console.configure(
            state="normal"
        )

        self.console.insert(
            "end",
            f"{hora}  {message}\n"
        )

        self.console.see("end")

        self.console.configure(
            state="disabled")