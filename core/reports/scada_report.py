from core.reports.base_report import BaseReport

from core.excel_manager import ExcelManager
from core.managers.scada_manager import ScadaManager
from core.managers.generation_manager import GenerationManager
from core.managers.image_manager import ImageManager


class ScadaReport(BaseReport):

    def run(self):

        resumen = {}

        excel = ExcelManager(self.master_file)

        try:

            self.notify("Creando backup...")

            backup = excel.create_backup()

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

                image_manager.replace_all([
                    scada.visualizers[i]
                    for i in range(1, 6)
                ])

            self.notify("Actualizando generación...")

            generation_result = generation.update(
                scada.first_visualizer
            )

            self.notify("Guardando libro...")

            excel.save()

            resumen = {
                "backup": backup,
                "scada": scada_result,
                "generation": generation_result,
                "success": True
            }

            self.notify("Proceso finalizado.")

        except Exception as e:

            resumen = {
                "success": False,
                "error": str(e)
            }

            self.notify(f"ERROR: {e}")

        finally:

            excel.close()

        return resumen