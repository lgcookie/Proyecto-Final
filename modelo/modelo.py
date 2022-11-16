from .sql_commands import PRUEBA_USARIO_EXISTE
from peewee import *
from datetime import date
from logger.log_decoradora import log_decoradora
import random
import string
from observadores.observador import Observador

db = SqliteDatabase("mi_base.db")

class BaseModel(Model):
    class Meta:
        database = db

class Usarios(BaseModel):
    id = AutoField()
    correo = CharField(unique=True)
    empresa = CharField(null = True)
    verificado = BooleanField()
    verifación_codigo = CharField(null = True)
    fecha_de_registrar = DateField()

    def __str__(self,):
        return "Usario "+ str(self.id) +"con email: "+self.correo+" que trabaja para: "

db.connect()
db.create_tables([Usarios])
cursor=db.cursor()



class Abmc(Usarios, Observador):
    def __init__(
        self,
    ):
        self.cursor=db.cursor()

    # Instaniciar el observador y agregar las funciones y los eventos que los escuchan 
        Observador.__init__(self)
        self.actualizar('alta_tbl',  self.alta_tbl)
        self.actualizar('borrar_tbl',  self.borrar_tbl)
        self.actualizar('verificar_tbl',  self.verificar_tbl)
        self.actualizar('actualizar_tbl',self.actualizar_tbl)
        
    ### Va a agregar un nuevo usario ###
    @log_decoradora   
    def alta_tbl(self,correo,empresa,verificado):

        exists = self.cursor.execute(PRUEBA_USARIO_EXISTE, (correo,))
        exists = True if self.cursor.fetchone()[0]==1 else False

        # Probar si el usario no has elegido un usario, levantar un error es así 
        if exists:
            raise Exception('Usario ya existe, por favor reintenté con un diferente correo')

        # Si el usuario ya es verificado va a generar un nuevo codigo de verifición por correo electronico
        if verificado:
            verifación_codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            usario=Usarios(correo=correo,empresa = empresa,fecha_de_registrar=date.today(), verificado=True,verifación_codigo=verifación_codigo)
            ### Todovía no he agregado la función para enviar el codigo
        else:
        
        # Si el usuario aún no verificado, va a dejar el campo de verificón vacio y setear verificado a falsa
            usario=Usarios(correo=correo,empresa = empresa,fecha_de_registrar=date.today(), verificado=False)

        # Guardar el usario objeto nuevo 
        usario.save()

        return {
            'msj': f'agregar usario {usario.id} con correo: {usario.correo} y empresa: {usario.empresa} con exito'
            }


    ### Cada vez hay una operación en la tabla, esta función va a actualizar la vista ###
    @log_decoradora  
    def actualizar_tbl(self, mitreeview):

        # limpieza de tabla original
        records = mitreeview.get_children()
        for element in records:
            mitreeview.delete(element)

        # consiguiendo datos
        for fila in Usarios.select():
            mitreeview.insert("", 0, text=fila.id, values=(fila.correo, fila.empresa, fila.verificado,fila.verifación_codigo,fila.fecha_de_registrar))
        return {
            'msj': f'actualizar la tabla con exito, hay {len(Usarios.select())} records en total'
        }

    ### Va a borrar el record desde la tabla ###
    @log_decoradora  
    def borrar_tbl(self, mitreeview):

        # Seleccionar el elemento destacado
        item_seleccionado = mitreeview.focus()
        valor_id = mitreeview.item(item_seleccionado)

        # Probar si el usario no has elegido un usario, levantar un error es así 
        if valor_id["text"] == "":
            raise Exception('No has elegido un usario, por favor reintenté')
        else:
            borrar=Usarios.get(Usarios.id==valor_id["text"])
            borrar.delete_instance()

            return {
                'msj': f'borrar el usario con usario_id: {valor_id["text"]} con exito'
            }

    ### Si el usuario todovía no es verificado, esta función se sirve para generar un código de verifición 
    # y despues disparar el controlador de correo ###
    @log_decoradora  
    def verificar_tbl(self,mitreeview):

        # Seleccionar el elemento destacado
        item_seleccionado = mitreeview.focus()
        valor_id = mitreeview.item(item_seleccionado)["text"]
        verifación_codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        actualizar=Usarios.update(verifación_codigo=verifación_codigo, verificado=True).where(Usarios.id==valor_id)
        actualizar.execute()
        ### Todovía no he agregado la función para enviar el codigo
        return {
            'msj': f'verificar el usario con usario_id: {valor_id} con exito'
        }
    
    def __str__(self):
        return 'Manejar los operacions por de base de datos.'

    