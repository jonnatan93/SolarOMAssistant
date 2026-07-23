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

    # Guarda la lista de visualizadores encontrados
        self.visualizers = None

        # ----------------------------------------------------

    def update(self, folder, callback=None):

        self.visualizers = FileDetector.find_visualizers(folder)

        archivos = self.visualizers

        self.first_visualizer = archivos[1]

        resumen = {}

        for numero in range(1, 6):

            if callback:
                callback(f"Visualizador {numero}")

            resultado = self.update_visualizer(
                archivos[numero],
                numero
            )

            resumen[numero] = resultado

        return resumen

    # ----------------------------------------------------

    def update_visualizer(self, visualizer_file, number):

        resultado = VisualizerReader.read(
            visualizer_file,
            number
        )

        destino = self.TABLES[number]

        self.clear_previous_data(
            destino,
            resultado["columns"]
        )

        self.sheet.range(destino).value = resultado["data"]

        return {
            "rows": resultado["rows"],
            "columns": resultado["columns"],
            "last_row": resultado["last_row"]
        }

    # ----------------------------------------------------

    def clear_previous_data(self, start_cell, columns):

        start = self.sheet.range(start_cell)

        start_row = start.row
        start_col = start.column

        end_row = start_row + 200
        end_col = start_col + columns - 1

        self.sheet.range(
            (start_row, start_col),
            (end_row, end_col)
        ).clear_contents()