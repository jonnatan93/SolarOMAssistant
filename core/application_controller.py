import threading
from tkinter import messagebox

from core.report_manager import ReportManager


class ApplicationController:

    def __init__(self, window):

        self.window = window

    # -----------------------------------------------------

    def start(self):

        self.window.run_button.configure(
            state="disabled",
            text="Procesando..."
        )

        self.window.status.set_status(
            "Ejecutando..."
        )

        self.window.clear_log()

        self.window.log_message(
            "========================================"
        )

        self.window.log_message(
            "Solar O&M Assistant iniciado."
        )

        hilo = threading.Thread(
            target=self.execute,
            daemon=True
        )

        hilo.start()

    # -----------------------------------------------------

    def execute(self):

        manager = ReportManager()

        report = manager.create(
             "PR",
            self.window.master_entry.get(),
            self.window.folder_entry.get(),
            callback=self.window.log_message
        )
        resultado = report.run()

        self.window.after(
        0,
        lambda: self.finish(resultado)
        )

    # -----------------------------------------------------

    def finish(self, resultado):

        self.window.run_button.configure(

            state="normal",

            text="Actualizar Informe"

        )

        if resultado["success"]:

            self.window.status.set_status(
                "Finalizado"
            )

            messagebox.showinfo(

                "Solar O&M Assistant",

                "Proceso terminado correctamente."

            )

        else:

            self.window.status.set_status(
                "Error"
            )

            messagebox.showerror(

                "Solar O&M Assistant",

                resultado["error"]

            )