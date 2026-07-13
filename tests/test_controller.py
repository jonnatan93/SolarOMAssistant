from core.automation_controller import AutomationController

LIBRO = r"C:\Users\OperadorCaiman\OneDrive - Enerland 2007 Fotovoltaica, S.L\Documentos\O&M\Registro de Variables\Registro de Variables_PR20260707.xlsm"

CARPETA = r"C:\Users\OperadorCaiman\Downloads\Nueva carpeta"


def progreso(mensaje):
    print(f">>> {mensaje}")


controller = AutomationController(
    LIBRO,
    CARPETA,
    callback=progreso
)

resultado = controller.run()

print("\n========== RESULTADO ==========")
print(resultado)