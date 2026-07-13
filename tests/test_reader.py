from core.visualizer_reader import VisualizerReader

archivo = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta\Visualizador de gráficas-20260707-1.xlsx"

resultado = VisualizerReader.read(
    archivo,
    1
)

print()

print("========== RESULTADO ==========")

print(f"Filas      : {resultado['rows']}")
print(f"Columnas   : {resultado['columns']}")
print(f"Última fila: {resultado['last_row']}")

print()

print("Primera fila:")

print(resultado["data"][0])

print()

print("Última fila:")

print(resultado["data"][-1])