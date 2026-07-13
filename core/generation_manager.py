from pathlib import Path
from datetime import datetime


class GenerationManager:

    SHEET_REGISTRO = "Registro de datos"

    SHEET_GENERACION = "Gen Medida Vs Esperada"

    CELL_GENERATION = "X101"

    DATE_COLUMN = "C"

    GENERATION_COLUMN = "D"

    def __init__(self, excel):

        self.excel = excel

        self.ws_registro = excel.sheet(self.SHEET_REGISTRO)

        self.ws_generacion = excel.sheet(self.SHEET_GENERACION)

    # --------------------------------------------------

    def update(self, visualizer_file):

        fecha = self.extract_date(visualizer_file)

        generacion = self.get_generation()

        fila = self.find_date(fecha)

        self.write_generation(
            fila,
            generacion
        )

        return {

            "date": fecha,

            "generation": generacion,

            "row": fila

        }

    # --------------------------------------------------

    def get_generation(self):

        valor = self.ws_registro.range(

            self.CELL_GENERATION

        ).value

        if valor is None:

            raise Exception(

                f"La celda {self.CELL_GENERATION} está vacía."

            )

        return float(valor)

    # --------------------------------------------------

    def extract_date(

        self,

        visualizer_file

    ):

        nombre = Path(

            visualizer_file

        ).stem

        partes = nombre.split("-")

        fecha = partes[-2]

        return datetime.strptime(

            fecha,

            "%Y%m%d"

        ).date()

    # --------------------------------------------------

    def find_date(

        self,

        report_date

    ):

        ultima = self.ws_generacion.used_range.last_cell.row

        for fila in range(2, ultima + 1):

            valor = self.ws_generacion.range(

                f"C{fila}"

            ).value

            if valor is None:

                continue

            if isinstance(

                valor,

                datetime

            ):

                valor = valor.date()

            if valor == report_date:

                return fila

        raise Exception(

            f"No se encontró la fecha {report_date}"

        )

    # --------------------------------------------------

    def write_generation(

        self,

        row,

        generation

    ):

        self.ws_generacion.range(

            f"D{row}"

        ).value = generation