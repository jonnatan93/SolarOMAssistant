from pathlib import Path


class FileDetector:

    @staticmethod
    def buscar_visualizadores(carpeta):

        carpeta = Path(carpeta)

        encontrados = {}

        for i in range(1, 6):

            archivos = list(carpeta.glob(f"*-{i}.xlsx"))

            encontrados[i] = len(archivos) > 0

        return encontrados