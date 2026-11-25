import threading
import traceback

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

            self.window.set_running_state(True)

            self.window.clear_log()

            self.window.set_progress(0)

            self.window.log_message("======================================")
            self.window.log_message("Solar O&M Assistant")
            self.window.log_message("Iniciando proceso...")
            self.window.log_message("======================================")

            master = self.window.master_entry.get()
            folder = self.window.folder_entry.get()
            report_type = self.window.get_selected_report_type()
            report_label = ReportManager.get_label(report_type)

            self.window.log_message(f"Actividad seleccionada: {report_label} ({report_type})")
            self.window.log_message(f"Libro maestro: {master}")
            self.window.log_message(f"Carpeta visualizadores: {folder}")

            self.window.set_progress(0.05)

            report = self.manager.create(
                report_type,
                master,
                folder,
                callback=self.window.log_message,
                progress_callback=self.window.set_progress
            )

            resultado = report.run()

            if resultado["success"]:

                self.window.set_progress(1.0)
                self.window.set_status("Finalizado correctamente")
                self.window.log_message("")
                self.window.log_message("✅ Proceso finalizado correctamente.")

            else:

                self.window.set_progress(0)
                self.window.set_status("Finalizado con errores")
                self.window.log_message("")
                self.window.log_message("❌ El proceso terminó con errores.")
                self.window.log_message(resultado["error"])

        except Exception:

            self.window.set_progress(0)
            self.window.set_status("Error no controlado")

            self.window.log_message("")
            self.window.log_message("======================================")
            self.window.log_message("❌ ERROR NO CONTROLADO")
            self.window.log_message("======================================")
            self.window.log_message(traceback.format_exc())
            self.window.log_message("======================================")

        finally:

            self.window.set_running_state(False)