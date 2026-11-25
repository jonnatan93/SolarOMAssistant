import xlwings as xw
from pathlib import Path


class ExcelManager:
    """
    Administra la conexión con Excel.

    NO contiene lógica del negocio.

    Solamente:

    - Abrir Excel
    - Abrir libro
    - Guardar
    - Cerrar
    - Obtener hojas
    """

    def __init__(self, master_file):

        self.master_file = Path(master_file)

        if not self.master_file.exists():
            raise FileNotFoundError(
                f"No existe el archivo:\n{self.master_file}"
            )

        self.app = None
        self.book = None

    # ---------------------------------------------------

    def open(self):

        if self.book is not None:
            return

        self.app = xw.App(
            visible=False,
            add_book=False
        )

        self.app.display_alerts = False
        self.app.screen_updating = False

        self.book = self.app.books.open(
            str(self.master_file)
        )

    # ---------------------------------------------------

        # ---------------------------------------------------

    def sheet(self, sheet_name):

        for sh in self.book.sheets:

            if sh.name.strip() == sheet_name.strip():

                return sh

        disponibles = [repr(sh.name) for sh in self.book.sheets]

        raise Exception(
            f"No se encontró la hoja '{sheet_name}'.\n"
            f"Hojas disponibles:\n{disponibles}"
        )

    # ---------------------------------------------------

    def clear_table_data(self, sheet, start_cell, columns):
        """
        Limpia el contenido de una tabla desde start_cell hasta la última fila
        usada en la hoja, cubriendo exactamente `columns` columnas.
        """

        if columns <= 0:
            return

        start = sheet.range(start_cell)

        start_row = start.row
        start_col = start.column

        last_row = max(start_row, sheet.used_range.last_cell.row)
        end_col = start_col + columns - 1

        sheet.range(
            (start_row, start_col),
            (last_row, end_col)
        ).clear_contents()

    # ---------------------------------------------------

    # ---------------------------------------------------

    def save(self):

        self.book.save()

    # ---------------------------------------------------

    def close(self):

        if self.book:

            self.book.close()

            self.book = None

        if self.app:

            self.app.quit()

            self.app = None

    # ---------------------------------------------------

    def __enter__(self):

        self.open()

        return self

    # ---------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        self.close()