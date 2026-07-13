import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path

from core.config_manager import ConfigManager

from ui.theme import (
    APP_WIDTH,
    APP_HEIGHT,
    TITLE,
    FONT_TITLE,
    FONT_SUBTITLE,
    PADDING
)

from ui.components import (
    SectionTitle,
    StatusLabel
)


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(TITLE)

        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        self.minsize(APP_WIDTH, APP_HEIGHT)

        # ---------------- Configuración ----------------

        self.config_data = ConfigManager.load()

        # ---------------- Título ----------------

        title = ctk.CTkLabel(
            self,
            text="☀ Solar O&M Assistant",
            font=FONT_TITLE
        )

        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Automatización de Informes O&M",
            font=FONT_SUBTITLE
        )

        subtitle.pack()

        # ---------------- Contenedor ----------------

        self.container = ctk.CTkFrame(self)

        self.container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.build_paths()

        self.build_status()

        self.build_log()

        self.build_button()

        self.validate()

    # --------------------------------------------------

    def build_paths(self):

        SectionTitle(
            self.container,
            text="📄 Libro Maestro"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(20, 5)
        )

        frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        frame.pack(fill="x", padx=PADDING)

        self.master_entry = ctk.CTkEntry(frame)

        self.master_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.master_entry.insert(
            0,
            self.config_data["master_file"]
        )

        ctk.CTkButton(
            frame,
            text="Examinar",
            width=120,
            command=self.select_master
        ).pack(side="left", padx=10)

        # ------------------------------

        SectionTitle(
            self.container,
            text="📁 Carpeta Visualizadores"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(20, 5)
        )

        frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        frame.pack(fill="x", padx=PADDING)

        self.folder_entry = ctk.CTkEntry(frame)

        self.folder_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.folder_entry.insert(
            0,
            self.config_data["visualizer_folder"]
        )

        ctk.CTkButton(
            frame,
            text="Examinar",
            width=120,
            command=self.select_folder
        ).pack(side="left", padx=10)

    # --------------------------------------------------

    def build_status(self):

        SectionTitle(
            self.container,
            text="Estado"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(25, 5)
        )

        self.status = StatusLabel(
            self.container
        )

        self.status.pack(
            anchor="w",
            padx=PADDING
        )

    # --------------------------------------------------

    def build_log(self):

        SectionTitle(
            self.container,
            text="Registro"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(25, 5)
        )

        self.log = ctk.CTkTextbox(
            self.container,
            height=220
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=PADDING
        )

        self.log.insert(
            "end",
            "Esperando ejecución...\n"
        )

        self.log.configure(
            state="disabled"
        )

    # --------------------------------------------------

    def build_button(self):

        self.run_button = ctk.CTkButton(
            self.container,
            text="Actualizar Informe",
            height=45,
            state="disabled"
        )

        self.run_button.pack(
            pady=20
        )

    # --------------------------------------------------

    def select_master(self):

        filename = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsm *.xlsx")]
        )

        if not filename:
            return

        self.master_entry.delete(0, "end")

        self.master_entry.insert(0, filename)

        self.config_data["master_file"] = filename

        ConfigManager.save(self.config_data)

        self.validate()

    # --------------------------------------------------

    def select_folder(self):

        folder = filedialog.askdirectory()

        if not folder:
            return

        self.folder_entry.delete(0, "end")

        self.folder_entry.insert(0, folder)

        self.config_data["visualizer_folder"] = folder

        ConfigManager.save(self.config_data)

        self.validate()

    # --------------------------------------------------

    def validate(self):

        master_ok = Path(
            self.master_entry.get()
        ).exists()

        folder_ok = Path(
            self.folder_entry.get()
        ).exists()

        if master_ok and folder_ok:

            self.status.set_status(
                "Listo para iniciar"
            )

            self.run_button.configure(
                state="normal"
            )

        else:

            self.status.set_status(
                "Seleccione rutas válidas"
            )

            self.run_button.configure(
                state="disabled"
            )