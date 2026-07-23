import xlwings as xw

VISUALIZADOR = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-1.xlsx"
MAESTRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

app = xw.App(visible=False)
app.display_alerts = False

try:
    wb_visualizador = app.books.open(VISUALIZADOR)
    wb_maestro = app.books.open(MAESTRO)

    print("\n======= COM Pictures =======")

pictures = hoja_scada.api.Pictures()

print("Cantidad:", pictures.Count)

for i in range(1, pictures.Count + 1):

    pic = pictures.Item(i)

    print("---------------------")
    print("Índice :", i)
    print("Nombre :", pic.Name)
    print("Left   :", pic.Left)
    print("Top    :", pic.Top)
    print("Width  :", pic.Width)
    print("Height :", pic.Height)

    hoja_visualizador = wb_visualizador.sheets[0]
    hoja_scada = wb_maestro.sheets["Scada"]

    print(f"Imágenes en visualizador: {len(hoja_visualizador.pictures)}")
    print(f"Imágenes en hoja Scada: {len(hoja_scada.pictures)}")

    print("\n================ VISUALIZADOR ================")

    for i, pic in enumerate(hoja_visualizador.pictures, start=1):
        print(f"\nImagen {i}")
        print(f"Nombre : {pic.name}")
        print(f"Left   : {pic.left}")
        print(f"Top    : {pic.top}")
        print(f"Width  : {pic.width}")
        print(f"Height : {pic.height}")

    print("\n================ MAESTRO ====================")

    for i, pic in enumerate(hoja_scada.pictures, start=1):
        print(f"\nImagen {i}")
        print(f"Nombre : {pic.name}")
        print(f"Left   : {pic.left}")
        print(f"Top    : {pic.top}")
        print(f"Width  : {pic.width}")
        print(f"Height : {pic.height}")

finally:
    wb_visualizador.close()
    wb_maestro.close()
    app.quit()

print("\nPrueba finalizada.")