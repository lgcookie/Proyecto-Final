import logging
import os 
import socket
from io import StringIO
import logging.handlers
from cliente.log_cliente import ClienteLogger


stream = StringIO()
class CustomFormatter(logging.Formatter):
    """ Custom Formatter hace estes 2 cosas:
    1. Sobrecargo el 'funcName' con el valor de 'func_name_override', si existe.
    2. Sobrecargo 'filename' con el valor de 'file_name_override', si existe.
    """

    def format(self, record):
        if hasattr(record, 'funcion_nombre_anular'):
            record.funcName = record.funcion_nombre_anular
        if hasattr(record, 'archivo_nombre_anular'):
            record.filename = record.archivo_nombre_anular
        return super(CustomFormatter, self).format(record)

class CustomSocketHandler(logging.Handler):

    def __init__(self) -> None:
        self.mandar_msg = ClienteLogger().cliente_logger
        super().__init__()

    def emit(self, record):
        message = self.format(record)
        self.mandar_msg(message)

def get_logger(log_file_name, log_sub_dir):
    """ Crear un Log Archivo y retornar el Logger objeto """
    # Construir el Log Archivo path completo
    logPath = log_file_name if os.path.exists(log_file_name) else os.path.join(log_sub_dir,'logs', (str(log_file_name) + '.txt'))

    # Crear logger objeto y setear el format para logging y otros atributos
    logger = logging.Logger(log_file_name)

    # Retorna logger object
    handler = logging.FileHandler(logPath, 'a+')

    """ Setear el formatter de 'CustomFormatter' tipo desde tenemos que notar el log base función nombre y base archivo nombre """
    handler.setFormatter(CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s'))
    logger.addHandler(handler)
    # Setear el nivel del logger
    logger.setLevel(logging.NOTSET)

    socket_handler = CustomSocketHandler()  
    logger.addHandler(socket_handler)
    
    

    return logger