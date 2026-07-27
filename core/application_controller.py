import threading
from pathlib import Path

from core.report_manager import ReportManager


class ApplicationController:

    def __init__(self, window):

        self.window = window
        self.manager = ReportManager()

    # ----------------------------------------------------

    def start(self):

        threading.Thread(
            target=self.run,
            daemon=True
        ).start()

    # ----------------------------------------------------

    def run(self):

        try:

            self.window.run_button.configure(state="disabled")

            self.window.clear_log()
            self.window.log_message("Iniciando proceso...")

            master = self.window.master_entry.get()
            folder = self.window.folder_entry.get()

            report_type = self.detect_report(master)

            self.window.log_message(
                f"Tipo de informe detectado: {report_type}"
            )

            report = self.manager.create(
                report_type,
                master,
                folder,
                callback=self.window.log_message
            )

            resultado = report.run()

            if resultado["success"]:

                self.window.log_message(
                    "Proceso finalizado correctamente."
                )

            else:

                self.window.log_message(
                    resultado["error"]
                )

        except Exception as e:

            self.window.log_message(str(e))

        finally:

            self.window.run_button.configure(state="normal")

    # ----------------------------------------------------

    def detect_report(self, master_file):

        nombre = Path(master_file).stem.upper()

        if "PR" in nombre:
            return "PR"

        return "SCADA"