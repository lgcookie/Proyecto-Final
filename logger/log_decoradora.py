import sys, os
# from controler import DIRECTIO_RAIZ
from .logger import get_logger
from inspect import getframeinfo, stack
from datetime import date 


def log_decoradora(funcion):

    logger = get_logger(str(date.today()),os.path.dirname(os.path.abspath(__file__)))

    def func(*args,**kwargs):
        py_archivo_llamador = getframeinfo(stack()[1][0])
        extra_args = { 'funcion_nombre_anular': funcion.__name__,
                        'archivo_nombre_anular': os.path.basename(py_archivo_llamador.filename)}
 
        logger.info("Comenzando la interacción con la base de datos", extra = extra_args)
        try:
            """ log retorna valor desde el funcion """
            valor = funcion(*args, **kwargs)
            logger.info(f"Devuelto: {valor['msj']} - Terminar funcion", extra = extra_args)
            
            return valor
        except Exception as e:

            """log excepción si occurio el dentro la función"""
            logger.error(f"Excepcion: {str(sys.exc_info()[1])}", extra = extra_args)
            raise
    return func

