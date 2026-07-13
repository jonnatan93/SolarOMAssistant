import customtkinter as ctk

from ui.status_panel import StatusPanel

app = ctk.CTk()

app.geometry("600x250")

panel = StatusPanel(app)

panel.pack(fill="x", padx=20, pady=20)

panel.running()

app.after(1000, panel.backup)
app.after(2000, panel.scada)
app.after(3000, panel.generation)
app.after(4000, panel.saving)
app.after(5000, panel.success)

app.mainloop()