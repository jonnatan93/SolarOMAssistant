from core.visualizer_reader import VisualizerReader
from core.file_detector import FileDetector


class PRManager:

    SHEET = "Scada"

    DESTINO = "B7"

    def __init__(self, excel):

        self.excel = excel
        self.sheet = excel.sheet(self.SHEET)

        self.visualizer = None

    # -----------------------------------------------------

    def update(self, folder, callback=None):

        archivos = FileDetector.find_visualizers(
            folder,
            numbers=[6]
        )

        self.visualizer = archivos[6]

        if callback:
            callback("Leyendo Visualizador 6...")

        resultado = VisualizerReader.read(
            self.visualizer,
            6
        )

        self.clear_previous_data(
            self.DESTINO,
            resultado["columns"]
        )

        self.sheet.range(
            self.DESTINO
        ).value = resultado["data"]

        return {
            "rows": resultado["rows"],
            "columns": resultado["columns"],
            "last_row": resultado["last_row"]
        }

    # -----------------------------------------------------

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