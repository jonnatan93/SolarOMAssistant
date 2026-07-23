from core.reports.scada_report import ScadaReport
from core.reports.pr_report import PRReport


class ReportManager:

    def create(
        self,
        report_type,
        master_file,
        folder,
        callback=None
    ):

        if report_type == "SCADA":

            return ScadaReport(
                master_file,
                folder,
                callback
            )

        elif report_type == "PR":

            return PRReport(
                master_file,
                folder,
                callback
            )

        raise ValueError(
            f"Reporte no soportado: {report_type}"
        )