from tkinter import StringVar
from tkinter import IntVar
from tkinter import Frame
from tkinter import BooleanVar
from tkinter import ttk
import os
import sys
import threading
from pathlib import Path
from logger.log_decoradora import log_decoradora
from cliente.log_cliente import ClienteLogger
from .validar import Validar
from modelo.modelo import Abmc
from observadores.observador import Evento
import socket
import subprocess

theproc=""

class Ventanita(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self)
        self.root = window
        self.correo = StringVar()
        self.empresa = StringVar()
        self.radio_var =IntVar()
        self.verificado = BooleanVar()
        self.a = IntVar()
        self.opcion = StringVar()
        self.f = Frame(self.root)
        self.tree = ttk.Treeview(self.f)
        self.objeto_base = Abmc()
        # Frame
        self.root.title("Proyecto Final")
        self.f.config(width=1020, height=1020)
        self.f.grid(row=10, column=0, columnspan=4)

        # Etiquetas
        self.superior = ttk.Label(
            self.root, text="Ingrese los datos", width=40, font=("-size", 14, "-weight", "bold")
        )
        self.usuario_correo = ttk.Label(self.root, text="Usuario Email", font=("-size", 14, "-weight", "bold"))
        self.usuario_empresa = ttk.Label(self.root, text="Usuario Empresa", font=("-size", 14, "-weight", "bold"))
        self.usuario_verificado = ttk.Label(self.root, text="Usuario Verificado", font=("-size", 14, "-weight", "bold"))
        self.registros = ttk.Label(
            self.root, text="Usuarios que ya existen", justify="center",
            font=("-size", 21, "-weight", "bold")
        )

        # Agrego ruta a servidor
        self.raiz = Path(__file__).resolve().parent
        self.ruta_server= os.path.join(os.getcwd(),"servidor","log_servidor.py")
        self.superior.grid(
            row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e"
        )
        self.usuario_correo.grid(row=1, column=0, sticky="w")
        self.usuario_empresa.grid(row=2, column=0, sticky="w")
        self.usuario_verificado.grid(row=3, column=0, sticky="w")
        self.registros.grid(
            row=4, column=1, columnspan=1, padx=0, pady=0,
        )
        
        self.Ent1 = ttk.Entry(self.root,textvariable=self.correo)
        self.Ent1.grid(row=1, column=1,pady=1)
        self.Ent2 = ttk.Entry(self.root, textvariable=self.empresa)
        self.Ent2.grid(row=2, column=1,pady=1)
        self.Ent3 = ttk.Checkbutton(self.root, variable=self.verificado, onvalue=True,offvalue=False)
        self.Ent3.grid(row=3, column=1,pady=1)

        # Botones
        self.boton_alta = ttk.Button(self.root, text="Aggregar", style="Toggle.TButton", command=lambda: self.alta())
        self.boton_alta.grid(row=6, column=0, padx=1, pady=3)

        self.boton_editar = ttk.Button(
            self.root, text="Verificar", style="Toggle.TButton", command=lambda: self.verificar()
        )
        self.boton_editar.grid(row=6, column=1, padx=1, pady=3)

        self.boton_borrar = ttk.Button(
            self.root, text="Borrar", style="Toggle.TButton", command=lambda: self.borrar()
        )
        self.boton_borrar.grid(row=6, column=2, padx=1, pady=3)
        
        self.boton_activar = ttk.Radiobutton(self.root, text="Activar Logs", command=lambda: self.intentar_conexión(), variable= self.radio_var, value=1)
        self.boton_activar.grid(row=2, column=3, padx=1, pady=3)

        self.boton_desactivar = ttk.Radiobutton(self.root, text="Desactivar Logs",command=lambda: self.desactivar_log_servidor(),variable= self.radio_var, value=0)
        self.boton_desactivar.grid(row=3, column=3, padx=1, pady=3)
        # Tree
        self.tree["columns"] = ("col1", "col2", "col3","col4","col5")
        self.tree.column("#0", width=20, minwidth=50, anchor="c")
        self.tree.column("col1", width=140, minwidth=50,anchor="c")
        self.tree.column("col2", width=90, minwidth=50,anchor="c")
        self.tree.column("col3", width=140, minwidth=50,anchor="c")
        self.tree.column("col4", width=140, minwidth=50,anchor="c")
        self.tree.column("col5", width=140, minwidth=50,anchor="c")
        self.tree.heading("#0", text="User ID")
        self.tree.heading("col1", text="Correo")
        self.tree.heading("col2", text="Empresa")
        self.tree.heading("col3", text="Verificado")
        self.tree.heading("col4", text="Codigo de Verifición")
        self.tree.heading("col5", text="La Fecha de Registrada")
        self.tree.grid(row=10, column=0, columnspan=4)

    def tbl_envoltura(func=None):
        def inner(self):
            func(self)
            Evento('actualizar_tbl', [self.tree])
        return inner

    
    @tbl_envoltura
    def alta(
        self,
    ):  
        if Validar.regex_correo(self.correo.get()) and Validar.regex_empresa(self.empresa.get()):
            Evento('alta_tbl', [self.correo.get(), self.empresa.get(), self.verificado.get()])

    
    @tbl_envoltura
    def borrar(
        self,
    ):  
        Evento('borrar_tbl', [self.tree])


    @tbl_envoltura
    def verificar(
        self,
    ):
        Evento('verificar_tbl', [self.tree])
    
    def intentar_conexión(self):

        ClienteLogger.log_servidor = True
        if theproc != "":
            theproc.kill()
            threading.Thread(target=self.activar_log_servidor, args=(True,), daemon=True).start()
        else:
            threading.Thread(target=self.activar_log_servidor, args=(True,), daemon=True).start()

    def activar_log_servidor(self,var):
        
        the_path = self.ruta_server
        if var==True:
            global theproc
            print("activated!")
            theproc = subprocess.Popen([sys.executable,the_path])
            theproc.communicate()
    
    def desactivar_log_servidor(self,):

        ClienteLogger.log_servidor = False
        global theproc

        if theproc !="":
            theproc.kill()
    
    
    
    
    


