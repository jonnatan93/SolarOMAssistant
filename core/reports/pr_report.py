from core.reports.base_report import BaseReport

from core.excel_manager import ExcelManager
from core.managers.pr_manager import PRManager
from core.managers.image_manager import ImageManager


class PRReport(BaseReport):

    def run(self):

        resumen = {}

        excel = ExcelManager(self.master_file)

        try:

            self.notify("Creando backup...")

            backup = excel.create_backup()

            self.notify("Abriendo libro Excel...")

            excel.open()

            manager = PRManager(excel)

            self.notify("Actualizando tabla PR...")

            pr_result = manager.update(
                self.folder,
                callback=self.callback
            )

            self.notify("Actualizando gráfica...")

            with ImageManager(excel.book) as image_manager:

                image_manager.replace_picture(
                    1,
                    manager.visualizer
                )

            self.notify("Guardando libro...")

            excel.save()

            resumen = {
                "backup": backup,
                "pr": pr_result,
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