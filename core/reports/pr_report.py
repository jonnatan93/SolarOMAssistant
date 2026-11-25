import traceback

from core.reports.base_report import BaseReport

from core.excel_manager import ExcelManager
from core.file_detector import FileDetector
from core.managers.pr_manager import PRManager
from core.managers.image_manager import ImageManager


class PRReport(BaseReport):

    def run(self):

        resumen = {}

        excel = None

        try:

            self.notify("Validando libro maestro y Visualizador 6...")
            self.report_progress(0.10)

            excel = ExcelManager(self.master_file)
            visualizers = FileDetector.find_visualizers(
                self.folder,
                numbers=[6]
            )

            self.notify("Abriendo libro Excel...")
            self.report_progress(0.25)

            excel.open()

            manager = PRManager(excel)

            self.notify("Actualizando tabla PR...")
            self.report_progress(0.45)

            pr_result = manager.update(
                self.folder,
                callback=self.callback,
                visualizers=visualizers
            )

            self.notify("Actualizando gráfica...")
            self.report_progress(0.75)

            with ImageManager(excel.book) as image_manager:

                image_manager.replace_picture(
                    1,
                    manager.visualizer
                )

            self.notify("Guardando libro...")
            self.report_progress(0.92)

            excel.save()

            resumen = {
                "pr": pr_result,
                "success": True
            }

            self.notify("Proceso finalizado.")

        except Exception:

            error = traceback.format_exc()

            resumen = {
                "success": False,
                "error": error
            }

            self.notify("")
            self.notify("========== ERROR ==========")
            self.notify(error)
            self.notify("===========================")

        finally:

            if excel is not None:
                excel.close()

        return resumen