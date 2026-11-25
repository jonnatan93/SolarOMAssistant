from core.visualizer_reader import VisualizerReader
from core.file_detector import FileDetector


class ScadaManager:

    SHEET = "Scada"

    TABLES = {
        1: "C7",
        2: "AA7",
        3: "BE7",
        4: "DI7",
        5: "DV7"
    }

    def __init__(self, excel):

        self.excel = excel

        self.sheet = excel.sheet(self.SHEET)

        self.first_visualizer = None

        # Guarda los visualizadores encontrados
        self.visualizers = {}

    # ----------------------------------------------------

    def update(
        self,
        folder,
        callback=None,
        visualizers=None,
        progress_callback=None
    ):

        self.visualizers = (
            visualizers
            if visualizers is not None
            else FileDetector.find_visualizers(folder)
        )

        self.first_visualizer = self.visualizers[1]

        resumen = {}
        total = len(self.visualizers)

        for idx, (numero, archivo) in enumerate(
            self.visualizers.items(),
            start=1
        ):

            if callback:
                callback(f"Leyendo y actualizando Visualizador {numero}...")

            resultado = self.update_visualizer(
                archivo,
                numero
            )

            resumen[numero] = resultado

            if progress_callback and total > 0:
                progress_callback(idx / total)

        return resumen

    # ----------------------------------------------------

    def update_visualizer(
        self,
        visualizer_file,
        number
    ):

        resultado = VisualizerReader.read(
            visualizer_file,
            number
        )

        destino = self.TABLES[number]

        self.excel.clear_table_data(
            self.sheet,
            destino,
            resultado["columns"]
        )

        self.sheet.range(destino).value = resultado["data"]

        return {
            "rows": resultado["rows"],
            "columns": resultado["columns"],
            "last_row": resultado["last_row"]
        }