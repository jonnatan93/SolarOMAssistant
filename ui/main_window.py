import customtkinter as ctk
from tkinter import filedialog

from core.config_manager import ConfigManager


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Solar O&M Assistant")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.config_data = ConfigManager.load()

        titulo = ctk.CTkLabel(
            self,
            text="☀ Solar O&M Assistant",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------- Libro maestro ----------------

        ctk.CTkLabel(frame, text="Libro Maestro").pack(anchor="w", padx=20, pady=(20, 5))

        self.master_entry = ctk.CTkEntry(frame, width=650)
        self.master_entry.pack(padx=20)
        self.master_entry.insert(0, self.config_data["master_file"])

        ctk.CTkButton(
            frame,
            text="Seleccionar Libro",
            command=self.select_master
        ).pack(pady=10)

        # ---------------- Carpeta ----------------

        ctk.CTkLabel(frame, text="Carpeta Visualizadores").pack(anchor="w", padx=20, pady=(20, 5))

        self.folder_entry = ctk.CTkEntry(frame, width=650)
        self.folder_entry.pack(padx=20)
        self.folder_entry.insert(0, self.config_data["visualizer_folder"])

        ctk.CTkButton(
            frame,
            text="Seleccionar Carpeta",
            command=self.select_folder
        ).pack(pady=10)
        self.estado_archivos = ctk.CTkTextbox(
    frame,
    width=650,
    height=160
)

self.estado_archivos.pack(pady=20)
self.status = ctk.CTkLabel(
            frame,
            text="Esperando..."
        )

        self.status.pack(pady=30)

        self.run_button = ctk.CTkButton(
            frame,
            text="Actualizar Informe",
            state="disabled"
        )

        self.run_button.pack()

        self.validate()

    def select_master(self):

        filename = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsm *.xlsx")]
        )

        if filename:

            self.master_entry.delete(0, "end")
            self.master_entry.insert(0, filename)

            self.config_data["master_file"] = filename
            ConfigManager.save(self.config_data)

            self.validate()

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

            self.config_data["visualizer_folder"] = folder
            ConfigManager.save(self.config_data)

            self.validate()

    def validate(self):

        if self.master_entry.get() and self.folder_entry.get():

            self.status.configure(text="✅ Listo para iniciar")
            self.run_button.configure(state="normal")

        else:

            self.status.configure(text="⚠ Seleccione el libro y la carpeta")
            self.run_button.configure(state="disabled")
from core.file_detector import FileDetector