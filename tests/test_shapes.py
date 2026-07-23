import xlwings as xw

MAESTRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

app = xw.App(visible=False)

try:
    wb = app.books.open(MAESTRO)
    sheet = wb.sheets["Scada"]

    shapes = sheet.api.Shapes

    print(f"Cantidad de Shapes: {shapes.Count}")

    for i in range(1, shapes.Count + 1):
        shp = shapes.Item(i)

        print("-------------------------")
        print("Índice :", i)
        print("Nombre :", shp.Name)
        print("Tipo   :", shp.Type)
        print("Left   :", shp.Left)
        print("Top    :", shp.Top)
        print("Width  :", shp.Width)
        print("Height :", shp.Height)

finally:
    wb.close()
    app.quit()