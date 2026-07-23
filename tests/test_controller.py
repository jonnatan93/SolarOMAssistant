from core.report_manager import ReportManager

LIBRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

CARPETA = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta"


def progreso(mensaje):
    print(f">>> {mensaje}")


manager = ReportManager()

report = manager.create(
    "SCADA",
    LIBRO,
    CARPETA,
    callback=progreso
)

resultado = report.run()

print("\n========== RESULTADO ==========")
print(resultado)