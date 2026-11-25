from core.reports.base_report import BaseReport

from core.excel_manager import ExcelManager
from core.file_detector import FileDetector
from core.managers.scada_manager import ScadaManager
from core.managers.generation_manager import GenerationManager
from core.managers.image_manager import ImageManager

import traceback


class ScadaReport(BaseReport):

    def run(self):

        resumen = {}

        excel = None

        try:

            self.notify("Validando libro maestro y visualizadores...")
            self.report_progress(0.10)

            excel = ExcelManager(self.master_file)
            visualizers = FileDetector.find_visualizers(self.folder)

            self.notify("Abriendo libro Excel...")
            self.report_progress(0.20)

            excel.open()

            scada = ScadaManager(excel)

            generation = GenerationManager(excel)

            self.notify("Actualizando SCADA...")
            self.report_progress(0.25)

            scada_result = scada.update(
                self.folder,
                callback=self.callback,
                visualizers=visualizers,
                progress_callback=lambda ratio: self.report_progress(
                    0.25 + 0.40 * ratio
                )
            )

            self.notify("Actualizando gráficas...")
            self.report_progress(0.68)

            with ImageManager(excel.book) as image_manager:

                image_manager.replace_all(
                    list(scada.visualizers.values()),
                    callback=self.callback,
                    progress_callback=lambda ratio: self.report_progress(
                        0.68 + 0.17 * ratio
                    )
                )

            self.notify("Actualizando generación...")
            self.report_progress(0.88)

            generation_result = generation.update(
                scada.first_visualizer
            )

            self.notify("Guardando libro...")
            self.report_progress(0.95)

            excel.save()

            resumen = {
                "scada": scada_result,
                "generation": generation_result,
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