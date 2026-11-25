from core.reports.scada_report import ScadaReport
from core.reports.pr_report import PRReport


class ReportManager:

    REPORT_TYPES = {
        "SCADA": {
            "label": "Informe Diario - SCADA",
            "class": ScadaReport,
        },
        "PR": {
            "label": "Informe Diario - PR",
            "class": PRReport,
        },
    }

    @classmethod
    def get_report_options(cls):
        """Retorna un diccionario {etiqueta: clave} para el selector de UI."""
        return {
            info["label"]: key
            for key, info in cls.REPORT_TYPES.items()
        }

    @classmethod
    def get_label(cls, report_type):
        """Retorna la etiqueta legible para una clave de informe."""
        info = cls.REPORT_TYPES.get(report_type)
        return info["label"] if info else report_type

    def create(
        self,
        report_type,
        master_file,
        folder,
        callback=None
    ):

        info = self.REPORT_TYPES.get(report_type)

        if info is None:
            raise ValueError(
                f"Reporte no soportado: {report_type}"
            )

        report_class = info["class"]

        return report_class(
            master_file,
            folder,
            callback
        )