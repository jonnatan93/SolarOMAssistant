from core.reports.base_report import BaseReport

from core.excel_manager import ExcelManager
from core.managers.scada_manager import ScadaManager
from core.managers.generation_manager import GenerationManager
from core.managers.image_manager import ImageManager

import traceback


class ScadaReport(BaseReport):

    def run(self):

        resumen = {}

        excel = ExcelManager(self.master_file)

        try:

            self.notify("Abriendo libro Excel...")

            excel.open()

            scada = ScadaManager(excel)

            generation = GenerationManager(excel)

            self.notify("Actualizando SCADA...")

            scada_result = scada.update(
                self.folder,
                callback=self.callback
            )

            self.notify("Actualizando gráficas...")

            with ImageManager(excel.book) as image_manager:

                image_manager.replace_all(
                    scada.visualizers.values()
                )

            self.notify("Actualizando generación...")

            generation_result = generation.update(
                scada.first_visualizer
            )

            self.notify("Guardando libro...")

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

            excel.close()

        return resumen