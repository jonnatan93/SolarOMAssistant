from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string


class VisualizerReader:
    """
    Lee cualquiera de los cinco archivos Visualizador.
    """

    CONFIG = {
        1: {"last_column": "W"},
        2: {"last_column": "AD"},
        3: {"last_column": "BD"},
        4: {"last_column": "M"},
        5: {"last_column": "Q"},
        6: {"last_column": "N"},
    }

    START_ROW = 36
    START_COLUMN = 3  # Columna C

    @classmethod
    def read(cls, file_path: str, visualizer_number: int):

        if visualizer_number not in cls.CONFIG:
            raise ValueError(
                f"Visualizador {visualizer_number} no existe."
            )

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        workbook = load_workbook(
            filename=file_path,
            data_only=True
        )

        sheet = workbook["1"]

        last_row = cls._find_last_row(sheet)

        last_column = column_index_from_string(
            cls.CONFIG[visualizer_number]["last_column"]
        )

        data = []

        for row in sheet.iter_rows(
                min_row=cls.START_ROW,
                max_row=last_row,
                min_col=cls.START_COLUMN,
                max_col=last_column,
                values_only=True):

            data.append(list(row))

        workbook.close()

        return {
            "rows": len(data),
            "columns": last_column - cls.START_COLUMN + 1,
            "last_row": last_row,
            "data": data
        }

    @classmethod
    def _find_last_row(cls, sheet):

        row = sheet.max_row

        while row >= cls.START_ROW:

            if sheet[f"C{row}"].value not in ("", None):
                return row

            row -= 1

        return cls.START_ROW