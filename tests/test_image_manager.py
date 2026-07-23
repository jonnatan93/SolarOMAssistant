import xlwings as xw

from core.image_manager import ImageManager

MAESTRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

app = xw.App(visible=False)

try:

    wb = app.books.open(MAESTRO)

    manager = ImageManager(wb)

    manager.list_positions()

finally:

    wb.close()
    app.quit()