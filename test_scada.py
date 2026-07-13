from core.excel_manager import ExcelManager
from core.scada_manager import ScadaManager

LIBRO = r"C:\RUTA\Registro.xlsm"

CARPETA = r"C:\RUTA\Visualizadores"

excel = ExcelManager(LIBRO)

excel.create_backup()

excel.open()

scada = ScadaManager(excel)

resultado = scada.update(CARPETA)

excel.save()

excel.close()

print()

print("========= SCADA =========")

for numero, info in resultado.items():

    print(

        f"Visualizador {numero}: "

        f"{info['rows']} filas - "

        f"{info['columns']} columnas"

    )