from core.excel_manager import ExcelManager
from core.scada_manager import ScadaManager
from core.generation_manager import GenerationManager


class AutomationController:

    def __init__(self, master_file, folder, callback=None):

        self.master_file = master_file
        self.folder = folder
        self.callback = callback

    # ---------------------------------------------------------

    def notify(self, message):

        if self.callback:
            self.callback(message)

    # ---------------------------------------------------------

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