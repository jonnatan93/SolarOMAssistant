import xlwings as xw

FILE = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-1.xlsx"

app = xw.App(visible=False)

try:

    wb = app.books.open(FILE)

    ws = wb.sheets[0]

    shapes = ws.api.Shapes

    print(f"Cantidad: {shapes.Count}\n")

    for i in range(1, shapes.Count + 1):

        shp = shapes.Item(i)

        print(
            i,
            shp.Name,
            shp.Type,
            shp.Left,
            shp.Top,
            shp.Width,
            shp.Height
        )

finally:

    wb.close()
    app.quit()