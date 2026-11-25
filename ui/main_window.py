import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from core.application_controller import ApplicationController
from core.config_manager import ConfigManager
from core.report_manager import ReportManager

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
        self.controller = ApplicationController(self)

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

        self.build_report_selector()

        self.build_paths()

        self.build_status()

        self.build_progress()

        self.build_button()

        self.build_log()

        self.validate()

    # --------------------------------------------------

    def build_report_selector(self):

        SectionTitle(
            self.container,
            text="📋 Tipo de Actividad"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(15, 5)
        )

        self.report_options = ReportManager.get_report_options()

        labels = list(self.report_options.keys())

        saved_type = self.config_data.get("report_type", "SCADA")
        initial_label = ReportManager.get_label(saved_type)
        if initial_label not in self.report_options:
            initial_label = labels[0]

        self.report_selector = ctk.CTkOptionMenu(
            self.container,
            values=labels,
            command=self.on_report_type_change
        )

        self.report_selector.set(initial_label)

        self.report_selector.pack(
            fill="x",
            padx=PADDING
        )

    # --------------------------------------------------

    def on_report_type_change(self, selected_label):

        report_type = self.report_options.get(selected_label, "SCADA")
        self.config_data["report_type"] = report_type
        ConfigManager.save(self.config_data)

    # --------------------------------------------------

    def get_selected_report_type(self):

        selected_label = self.report_selector.get()
        return self.report_options.get(selected_label, "SCADA")

    # --------------------------------------------------

    def build_paths(self):

        SectionTitle(
            self.container,
            text="📄 Libro Maestro"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(15, 5)
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
            pady=(15, 5)
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
            pady=(15, 5)
        )

        self.status = StatusLabel(
            self.container
        )

        self.status.pack(
            anchor="w",
            padx=PADDING
        )
    def build_progress(self):

        self.progress = ctk.CTkProgressBar(self.container)

        self.progress.pack(
            fill="x",
            padx=PADDING,
            pady=(10, 10)
        )

        self.progress.set(0)
    # --------------------------------------------------

    def build_log(self):

        SectionTitle(
            self.container,
            text="Registro"
        ).pack(
            anchor="w",
            padx=PADDING,
            pady=(10, 5)
        )

        self.log = ctk.CTkTextbox(
            self.container,
            height=150
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=PADDING,
            pady=(0, 10)
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
                state="disabled",
                command=self.controller.start
            )

            self.run_button.pack(
                fill="x",
                padx=PADDING,
                pady=(10, 10)
            )

    # --------------------------------------------------

    def select_master(self):

        filename = filedialog.askopenfilename(
            title="Seleccione el libro maestro",
            filetypes=[
                ("Libros de Excel", "*.xlsm *.xlsx"),
                ("Libros con macros (*.xlsm)", "*.xlsm"),
                ("Libros de Excel (*.xlsx)", "*.xlsx"),
                ("Todos los archivos", "*.*"),
            ]
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
    def set_progress(self, value):

        self.after(
            0,
            lambda: self.progress.set(value)
        )

    def reset_progress(self):

        self.progress.set(0)
    # --------------------------------------------------

    def validate(self, update_status=True):

        master_text = self.master_entry.get().strip()
        folder_text = self.folder_entry.get().strip()

        master_ok = bool(master_text) and Path(master_text).is_file()

        folder_ok = bool(folder_text) and Path(folder_text).is_dir()

        if master_ok and folder_ok:

            if update_status:
                self.status.set_status(
                    "Listo para iniciar"
                )

            self.run_button.configure(
                state="normal"
            )

        else:

            if update_status:
                self.status.set_status(
                    "Seleccione rutas válidas"
                )

            self.run_button.configure(
                state="disabled"
            )
    # --------------------------------------------------

    def set_running_state(self, is_running):

        self.after(
            0,
            lambda: self._apply_running_state(is_running)
        )

    def _apply_running_state(self, is_running):

        if is_running:
            self.run_button.configure(state="disabled")
            self.report_selector.configure(state="disabled")
            self.status.set_status("Ejecutando...")
        else:
            self.report_selector.configure(state="normal")
            self.validate(update_status=False)

    def set_status(self, text):

        self.after(
            0,
            lambda: self.status.set_status(text)
        )

    def clear_log(self):

        self.after(0, self._clear_log)

    def _clear_log(self):

        self.log.configure(state="normal")

        self.log.delete("1.0", "end")

        self.log.configure(state="disabled")

    # --------------------------------------------------

    def log_message(self, message):

        self.after(
            0,
            lambda: self._append(message)
        )

    # --------------------------------------------------

    def _append(self, message):

        from datetime import datetime

        self.log.configure(state="normal")

        self.log.insert(
            "end",
            f"{datetime.now():%H:%M:%S}  {message}\n"
        )

        self.log.see("end")

        self.log.configure(state="disabled")
    