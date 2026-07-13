import customtkinter as ctk
from tkinter import filedialog


class PathSelector(ctk.CTkFrame):

    def __init__(
        self,
        master,
        title,
        button_text,
        initial_value="",
        select_folder=False,
        callback=None
    ):

        super().__init__(master)

        self.callback = callback
        self.select_folder = select_folder

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 15, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.entry = ctk.CTkEntry(row)

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        if initial_value:
            self.entry.insert(0, initial_value)

        self.button = ctk.CTkButton(
            row,
            text=button_text,
            width=120,
            command=self.select
        )

        self.button.pack(
            side="left",
            padx=(10, 0)
        )

    # -----------------------------------------------------

    def select(self):

        if self.select_folder:

            value = filedialog.askdirectory()

        else:

            value = filedialog.askopenfilename(
                filetypes=[
                    ("Excel", "*.xlsm *.xlsx")
                ]
            )

        if not value:
            return

        self.set(value)

        if self.callback:
            self.callback(value)

    # -----------------------------------------------------

    def get(self):

        return self.entry.get()

    # -----------------------------------------------------

    def set(self, value):

        self.entry.delete(0, "end")

        self.entry.insert(0, value)

    # -----------------------------------------------------

    def enable(self):

        self.entry.configure(state="normal")

        self.button.configure(state="normal")

    # -----------------------------------------------------

    def disable(self):

        self.entry.configure(state="disabled")

        self.button.configure(state="disabled")