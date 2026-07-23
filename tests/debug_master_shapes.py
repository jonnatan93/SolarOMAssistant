import xlwings as xw

MASTER = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

app = xw.App(visible=False)

try:
    wb = app.books.open(MASTER)
    ws = wb.sheets["Scada"]

    shapes = ws.api.Shapes

    print(f"Cantidad de Shapes: {shapes.Count}\n")

    datos = []

    for i in range(1, shapes.Count + 1):

        s = shapes.Item(i)

        datos.append({
            "index": i,
            "name": s.Name,
            "left": float(s.Left),
            "top": float(s.Top),
            "width": float(s.Width),
            "height": float(s.Height)
        })

    print("=== ORDEN INTERNO ===")

    for d in datos:
        print(
            f'{d["index"]} '
            f'Left={d["left"]:.2f} '
            f'Top={d["top"]:.2f}'
        )

    print("\n=== ORDEN VISUAL ===")

    orden = sorted(datos, key=lambda x: (x["top"], x["left"]))

    for pos, d in enumerate(orden, start=1):
        print(
            f'Visual {pos} <- Shape {d["index"]} '
            f'Left={d["left"]:.2f} '
            f'Top={d["top"]:.2f}'
        )

finally:
    wb.close()
    app.quit()