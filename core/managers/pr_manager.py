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

    def update(self, folder, callback=None, visualizers=None):

        archivos = (
            visualizers
            if visualizers is not None
            else FileDetector.find_visualizers(folder, numbers=[6])
        )

        self.visualizer = archivos[6]

        if callback:
            callback("Leyendo Visualizador 6...")

        resultado = VisualizerReader.read(
            self.visualizer,
            6
        )

        self.excel.clear_table_data(
            self.sheet,
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