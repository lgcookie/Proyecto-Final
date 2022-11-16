from tkinter import Tk
from tkinter import IntVar
from callback_personalizada import report_callback_exception
from observadores.observador import Evento 
from vista.vista import Ventanita


class Controller:
    """
    Está es la clase principal
    """

    def __init__(self, root):
        self.root_controler = root
        self.objeto_vista = Ventanita(self.root_controler)


if __name__ == "__main__":
    root_tk = Tk()
    Tk.report_callback_exception = report_callback_exception
    application = Controller(root_tk)

    
    Evento('actualizar_tbl', [application.objeto_vista.tree])

    # Setear el tema inicialx
    root_tk.tk.call("source", "tema/azure.tcl")
    root_tk.tk.call("set_theme", "dark")
    root_tk.mainloop()
