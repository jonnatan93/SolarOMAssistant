from core.excel_manager import ExcelManager
from core.generation_manager import GenerationManager

LIBRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

VISUALIZADOR = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-1.xlsx"

excel = ExcelManager(LIBRO)

excel.open()

generation = GenerationManager(excel)

resultado = generation.update(VISUALIZADOR)

excel.save()

excel.close()

print()

print(resultado)