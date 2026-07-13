import customtkinter as ctk

from ui.path_selector import PathSelector

app = ctk.CTk()

app.geometry("900x250")


def changed(path):
    print(path)


master = PathSelector(
    app,
    title="Libro Maestro",
    button_text="Examinar",
    callback=changed
)

master.pack(fill="x", padx=20, pady=10)

folder = PathSelector(
    app,
    title="Carpeta Visualizadores",
    button_text="Examinar",
    select_folder=True,
    callback=changed
)

folder.pack(fill="x", padx=20, pady=10)

app.mainloop()