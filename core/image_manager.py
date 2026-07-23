"""
image_manager.py

Manejo de reemplazo de imágenes del libro maestro SCADA.

Autor: Reescrito para SolarOMAssistant
"""

from __future__ import annotations

import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import xlwings as xw


class ImageManager:
    """
    Reemplaza las imágenes del libro maestro usando
    las imágenes contenidas en los archivos Visualizador.

    NO utiliza Copy/Paste.

    Utiliza:

        Shapes.AddPicture()

    para evitar problemas del portapapeles.

    Las posiciones se obtienen una sola vez al iniciar
    la clase y se mantienen mediante referencias COM.
    """

    def __init__(self, workbook: xw.Book):

        self.workbook = workbook

        self.sheet = self.workbook.sheets["Scada"]

        self.temp_dir = tempfile.mkdtemp(prefix="solarom_images_")

        self.positions = []

        self._load_master_shapes()


    # ---------------------------------------------------------
    # CARGA DE SHAPES DEL LIBRO MAESTRO
    # ---------------------------------------------------------

    def _load_master_shapes(self):

        """
        Obtiene las cinco imágenes del libro maestro.

        IMPORTANTE

        Excel NO guarda los Shapes
        en el mismo orden en que se ven.

        Por eso se ordenan usando Left.
        """

        shapes = self.sheet.api.Shapes

        temp_shapes = []

        for i in range(1, shapes.Count + 1):

            shp = shapes.Item(i)

            try:

                shape_type = int(shp.Type)

            except Exception:

                continue

            # Solo imágenes
            if shape_type != 13:
                continue

            temp_shapes.append({

                "shape": shp,

                "left": float(shp.Left),

                "top": float(shp.Top),

                "width": float(shp.Width),

                "height": float(shp.Height)

            })

        if len(temp_shapes) != 5:

            raise RuntimeError(
                f"Se esperaban 5 imágenes en el libro maestro y se encontraron {len(temp_shapes)}"
            )

        # Orden visual:
        # izquierda -> derecha

        temp_shapes.sort(key=lambda x: x["left"])

        self.positions = temp_shapes

        print("\nOrden visual detectado:\n")

        for idx, item in enumerate(self.positions, start=1):

            print(
                f"{idx} -> Left={item['left']:.2f}"
            )


    # ---------------------------------------------------------
    # EXTRACCIÓN DE IMAGEN DESDE VISUALIZADOR
    # ---------------------------------------------------------

    def _extract_image(self, visualizer_file: str):

        """
        Extrae la única imagen existente
        dentro del archivo Visualizador.

        Devuelve la ruta temporal.
        """

        visualizer_file = Path(visualizer_file)

        if not visualizer_file.exists():

            raise FileNotFoundError(
                visualizer_file
            )

        with zipfile.ZipFile(visualizer_file, "r") as z:

            media = [

                f

                for f in z.namelist()

                if f.startswith("xl/media/")

            ]

            if len(media) == 0:

                raise RuntimeError(
                    "No se encontró ninguna imagen en el Visualizador."
                )

            image_name = os.path.basename(media[0])

            destination = os.path.join(
                self.temp_dir,
                image_name
            )

            with z.open(media[0]) as src:

                with open(destination, "wb") as dst:

                    shutil.copyfileobj(src, dst)

            return destination
        # ---------------------------------------------------------
    # REEMPLAZAR UNA IMAGEN
    # ---------------------------------------------------------

    def replace_picture(
        self,
        index: int,
        visualizer_file: str
    ):
        """
        Reemplaza una de las cinco imágenes del libro maestro.

        index:
            1..5

        visualizer_file:
            Archivo Visualizador correspondiente.
        """

        if index < 1 or index > len(self.positions):

            raise ValueError(
                f"Índice inválido: {index}"
            )

        image_path = self._extract_image(
            visualizer_file
        )

        pos = self.positions[index - 1]

        old_shape = pos["shape"]

        left = pos["left"]
        top = pos["top"]
        width = pos["width"]
        height = pos["height"]

        try:

            old_shape.Delete()

        except Exception as e:

            raise RuntimeError(
                f"No fue posible eliminar la imagen {index}: {e}"
            )

        try:

            new_shape = self.sheet.api.Shapes.AddPicture(

                Filename=image_path,

                LinkToFile=False,

                SaveWithDocument=True,

                Left=left,

                Top=top,

                Width=width,

                Height=height

            )

        except Exception as e:

            raise RuntimeError(
                f"No fue posible insertar la imagen {index}: {e}"
            )

        pos["shape"] = new_shape

        try:

            new_shape.LockAspectRatio = False

        except Exception:
            pass

        try:

            new_shape.Placement = 1

        except Exception:
            pass

        print(
            f"Imagen {index} reemplazada correctamente."
        )


    # ---------------------------------------------------------
    # REEMPLAZAR VARIAS IMÁGENES
    # ---------------------------------------------------------

    def replace_multiple(
        self,
        visualizer_files
    ):
        """
        Reemplaza varias imágenes.

        visualizer_files debe contener exactamente
        cinco archivos.

        El orden esperado es:

            archivo-1
            archivo-2
            archivo-3
            archivo-4
            archivo-5
        """

        if len(visualizer_files) != 5:

            raise ValueError(
                "Se esperaban exactamente cinco archivos."
            )

        for index, file in enumerate(
            visualizer_files,
            start=1
        ):

            print(
                f"Procesando imagen {index}..."
            )

            self.replace_picture(
                index,
                file
            )

        print(
            "\nTodas las imágenes fueron reemplazadas."
        )


    # ---------------------------------------------------------
    # VALIDACIÓN
    # ---------------------------------------------------------

    def validate_shapes(self):
        """
        Imprime el estado actual
        de las referencias almacenadas.
        """

        print("\nEstado de imágenes:\n")

        for idx, item in enumerate(
            self.positions,
            start=1
        ):

            shp = item["shape"]

            try:

                print(

                    f"{idx}"

                    f"  Left={float(shp.Left):.2f}"

                    f"  Top={float(shp.Top):.2f}"

                    f"  Width={float(shp.Width):.2f}"

                    f"  Height={float(shp.Height):.2f}"

                )

            except Exception:

                print(
                    f"{idx} -> Shape inválido."
                )
        # ---------------------------------------------------------
    # REEMPLAZAR TODAS LAS IMÁGENES
    # ---------------------------------------------------------

    def replace_all_images(self, visualizer_files):
        """
        Reemplaza las cinco imágenes del libro maestro.

        visualizer_files debe ser una lista
        con cinco archivos Visualizador.
        """

        if len(visualizer_files) != 5:

            raise RuntimeError(
                "Se requieren exactamente cinco archivos."
            )

        print("\nIniciando reemplazo de imágenes...\n")

        for index, file in enumerate(
            visualizer_files,
            start=1
        ):

            print(
                f"[{index}/5] {Path(file).name}"
            )

            self.replace_picture(
                index,
                file
            )

        print("\nProceso finalizado correctamente.")


    # ---------------------------------------------------------
    # LIMPIEZA
    # ---------------------------------------------------------

    def cleanup(self):
        """
        Elimina los archivos temporales.
        """

        if hasattr(self, "temp_dir"):

            if os.path.exists(self.temp_dir):

                shutil.rmtree(
                    self.temp_dir,
                    ignore_errors=True
                )

                print(
                    "Archivos temporales eliminados."
                )


    # ---------------------------------------------------------
    # CONTEXTO
    # ---------------------------------------------------------

    def __enter__(self):

        return self


    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        self.cleanup()


    # ---------------------------------------------------------
    # DESTRUCTOR
    # ---------------------------------------------------------

    def __del__(self):

        try:

            self.cleanup()

        except Exception:

            pass


    # ---------------------------------------------------------
    # INFORMACIÓN
    # ---------------------------------------------------------

    def print_shapes(self):
        """
        Imprime el orden visual detectado.
        """

        print("\nShapes cargados:\n")

        for idx, item in enumerate(
            self.positions,
            start=1
        ):

            print(

                f"{idx}"

                f" Left={item['left']:.2f}"

                f" Top={item['top']:.2f}"

                f" Width={item['width']:.2f}"

                f" Height={item['height']:.2f}"

            )


    # ---------------------------------------------------------
    # CANTIDAD
    # ---------------------------------------------------------

    @property
    def count(self):

        return len(self.positions)


    # ---------------------------------------------------------
    # INDEXACIÓN
    # ---------------------------------------------------------

    def __getitem__(self, index):

        return self.positions[index]
        # ---------------------------------------------------------
    # COMPATIBILIDAD
    # ---------------------------------------------------------

    def replace_all(self, visualizer_files):
        """
        Alias para mantener compatibilidad con el proyecto.
        """

        return self.replace_all_images(visualizer_files)


    # ---------------------------------------------------------
    # REPRESENTACIÓN
    # ---------------------------------------------------------

    def __repr__(self):

        return (

            f"<ImageManager "

            f"imagenes={self.count}>"

        )