import customtkinter as ctk


class StatusPanel(ctk.CTkFrame):

    COLORS = {
        "waiting": "#808080",
        "running": "#F5A623",
        "success": "#3CB371",
        "error": "#E74C3C"
    }

    def __init__(self, master):

        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Estado",
            font=("Segoe UI", 15, "bold")
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.status = ctk.CTkLabel(
            self,
            text="● Esperando",
            anchor="w",
            text_color=self.COLORS["waiting"]
        )

        self.status.pack(
            anchor="w",
            padx=10
        )

        self.progress = ctk.CTkProgressBar(self)

        self.progress.pack(
            fill="x",
            padx=10,
            pady=15
        )

        self.progress.set(0)

    # ---------------------------------------------------------

    def waiting(self):

        self.status.configure(
            text="● Esperando",
            text_color=self.COLORS["waiting"]
        )

        self.progress.set(0)

    # ---------------------------------------------------------

    def running(self):

        self.status.configure(
            text="● Ejecutando...",
            text_color=self.COLORS["running"]
        )

        self.progress.set(0.15)

    # ---------------------------------------------------------

    def backup(self):

        self.progress.set(0.25)

    # ---------------------------------------------------------

    def scada(self):

        self.progress.set(0.70)

    # ---------------------------------------------------------

    def generation(self):

        self.progress.set(0.85)

    # ---------------------------------------------------------

    def saving(self):

        self.progress.set(0.95)

    # ---------------------------------------------------------

    def success(self):

        self.status.configure(
            text="● Finalizado",
            text_color=self.COLORS["success"]
        )

        self.progress.set(1)

    # ---------------------------------------------------------

    def error(self):

        self.status.configure(
            text="● Error",
            text_color=self.COLORS["error"]
        )

        self.progress.set(1)