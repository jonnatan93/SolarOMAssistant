import customtkinter as ctk

from ui.log_panel import LogPanel

app = ctk.CTk()

app.geometry("700x400")

panel = LogPanel(app)

panel.pack(fill="both", expand=True)

panel.log("Aplicación iniciada.")
panel.log("Leyendo visualizador 1...")
panel.log("Proceso finalizado.")

app.mainloop()