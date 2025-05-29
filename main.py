from package.sis_academico import SistemaAcademico
import tkinter as tk
from package.gui.app_gui import SistemaAcademicoGUI

if __name__ == "__main__":

    root = tk.Tk()
    app = SistemaAcademicoGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

    # sistema = SistemaAcademico()
    # sistema.loop()
