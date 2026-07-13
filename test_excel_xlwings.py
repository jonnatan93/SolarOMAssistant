from core.excel_manager import ExcelManager

LIBRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

manager = ExcelManager(LIBRO)

manager.open()

print("Libro abierto correctamente")

print()

print(manager.sheet("Scada").name)

manager.close()

print("Libro cerrado")