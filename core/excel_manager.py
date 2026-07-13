from pathlib import Path
from datetime import datetime
import shutil

from openpyxl import load_workbook

from core.visualizer_reader import VisualizerReader
from core.file_detector import FileDetector


class ExcelManager:

    TABLES = {
        1: {"sheet": "Scada", "cell": "C7"},
        2: {"sheet": "Scada", "cell": "AA7"},
        3: {"sheet": "Scada", "cell": "BE7"},
        4: {"sheet": "Scada", "cell": "DI7"},
        5: {"sheet": "Scada", "cell": "DV7"},
    }

    def __init__(self, master_file):
        self.master_file = Path(master_file)
        if not self.master_file.exists():
            raise FileNotFoundError(master_file)
        self.workbook = None

    def create_backup(self):
        backup = self.master_file.with_name(
            f"{self.master_file.stem}_BACKUP_{datetime.now():%Y%m%d_%H%M%S}{self.master_file.suffix}"
        )
        shutil.copy2(self.master_file, backup)
        return backup

    def open(self):
        self.workbook = load_workbook(
            self.master_file,
            keep_vba=True
        )

    def save(self):
        self.workbook.save(self.master_file)

    def close(self):
        if self.workbook:
            self.workbook.close()
            self.workbook = None

    def paste_visualizer(self, visualizer_file, number):
        result = VisualizerReader.read(visualizer_file, number)

        cfg = self.TABLES[number]
        ws = self.workbook[cfg["sheet"]]

        start = ws[cfg["cell"]]
        start_row = start.row
        start_col = start.column

        for r in range(start_row, start_row + 200):
            for c in range(start_col, start_col + result["columns"]):
                ws.cell(row=r, column=c).value = None

        for r, row in enumerate(result["data"]):
            for c, value in enumerate(row):
                ws.cell(
                    row=start_row + r,
                    column=start_col + c,
                    value=value
                )

        return {
            "rows": result["rows"],
            "columns": result["columns"],
            "last_row": result["last_row"]
        }

    def update_scada(self, folder):
        backup = self.create_backup()

        self.open()

        files = FileDetector.find_visualizers(folder)

        summary = {
            "backup": str(backup),
            "visualizers": {}
        }

        for number in range(1, 6):
            summary["visualizers"][number] = self.paste_visualizer(
                files[number],
                number
            )

        self.save()
        self.close()

        return summary

