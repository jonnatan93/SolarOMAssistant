import xlwings as xw
from pathlib import Path
from datetime import datetime
import shutil


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

    def create_backup(self):

        backup = self.master_file.with_name(

            f"{self.master_file.stem}_BACKUP_"
            f"{datetime.now():%Y%m%d_%H%M%S}"
            f"{self.master_file.suffix}"

        )

        shutil.copy2(
            self.master_file,
            backup
        )

        return backup

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

    def sheet(self, sheet_name):

        return self.book.sheets[sheet_name]

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