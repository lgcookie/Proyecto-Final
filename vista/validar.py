import re
from tkinter import messagebox

class Validar():
    def __init__(
        self
    ): pass
    

    @staticmethod
    def regex_correo(avalidar):
        reg = re.compile("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")

        if not reg.fullmatch(str(avalidar)):
            messagebox.showerror('Invalido Correo',
            "Correo debería solomenete tener numeros, letras, .'s y @ !")
        return reg.match(str(avalidar))

    @staticmethod
    def regex_empresa(avalidar):

        reg = re.compile("^[a-zA-Z0-9_ ]*$")

        if not reg.fullmatch(str(avalidar)):
            messagebox.showerror('Invalido Nombre de Empresa',
            "Empresa nombre solomenete tener letras y no numeros y caracteres especial")
        return reg.match(str(avalidar))

