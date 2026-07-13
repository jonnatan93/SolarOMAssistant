from core.excel_manager import ExcelManager

LIBRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

CARPETA = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta"

manager = ExcelManager(LIBRO)

resultado = manager.update_scada(CARPETA)

print()

print("========= SCADA =========")

print("Backup:")
print(resultado["backup"])

print()

for numero, info in resultado["visualizers"].items():

    print(
        f"Visualizador {numero}: "
        f"{info['rows']} filas - "
        f"{info['columns']} columnas"
    )