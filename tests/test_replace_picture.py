import time
import xlwings as xw

MAESTRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"
VISUALIZADOR = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-1.xlsx"

app = xw.App(visible=True)

wb_destino = app.books.open(MAESTRO)
wb_origen = app.books.open(VISUALIZADOR)

hoja_origen = wb_origen.sheets[0]
hoja_destino = wb_destino.sheets["Scada"]

# Activar hoja origen
hoja_origen.activate()

shape = hoja_origen.api.Shapes.Item(1)

print("Copiando...")
shape.Copy()

time.sleep(1)

# Activar hoja destino
hoja_destino.activate()

print("Pegando...")

hoja_destino.api.Paste()

print("Finalizado.")

input("Presiona ENTER para cerrar...")

wb_origen.close(False)
wb_destino.close(False)

app.quit()