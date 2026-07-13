from pathlib import Path


class FileDetector:

    @staticmethod
    def find_visualizers(folder):

        folder = Path(folder)

        if not folder.exists():
            raise FileNotFoundError(folder)

        archivos = {}

        for numero in range(1, 6):

            encontrados = list(
                folder.glob(f"*-{numero}.xlsx")
            )

            if len(encontrados) == 0:
                raise FileNotFoundError(
                    f"No se encontró el Visualizador {numero}"
                )

            if len(encontrados) > 1:
                raise Exception(
                    f"Hay más de un Visualizador {numero}"
                )

            archivos[numero] = encontrados[0]

        return archivos