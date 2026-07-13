import customtkinter as ctk


class SectionTitle(ctk.CTkLabel):

    def __init__(self, master, text):

        super().__init__(
            master,
            text=text,
            font=("Segoe UI", 15, "bold")
        )


class StatusLabel(ctk.CTkLabel):

    def __init__(self, master):

        super().__init__(
            master,
            text="● Esperando",
            anchor="w"
        )

    def set_status(self, text):

        self.configure(text=f"● {text}")