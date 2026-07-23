import xlwings as xw

from core.image_manager import ImageManager

MASTER = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

VISUALIZERS = [
    r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-1.xlsx",
    r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-2.xlsx",
    r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-3.xlsx",
    r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-4.xlsx",
    r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-5.xlsx",
]

app = xw.App(visible=True)

try:

    wb = app.books.open(MASTER)

    manager = ImageManager(wb)

    manager.replace_all(VISUALIZERS)

    print("\nProceso terminado correctamente.")

    input("\nRevise el resultado y presione ENTER...")

finally:

    manager.cleanup()
    wb.close()
    app.quit()