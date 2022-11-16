#Se importa el módulo
import socket
import logging
from datetime import date
import pathlib
import os

#instanciamos un objeto para trabajar con el socket
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Puerto y servidor que debe escuchar
ser.bind((socket.gethostname(), 9000))



# Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
ser.listen()

# Al ejecutar el guión crear el logger objeto para guardar los logs que recibe desde el cliente
path = pathlib.Path(__file__).parent.resolve()
LOG_PATH = os.path.join(path, "servidor_logs",str(date.today())+".log")
logging.basicConfig(
     filename=LOG_PATH,
     level=logging.INFO, 
     format= '[%(asctime)s] %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
    )

while True:
    #Instanciamos un objeto cli (socket cliente) para recibir datos
    cli, addr = ser.accept()
    
    
    #Recibimos el mensaje, con el metodo recv recibimos datos. Por parametro la cantidad de bytes para recibir
    data = cli.recv(1024)
    if not data:
        break

    # Decode el mensaje y despúes de ponerlo en un archivo al través el logger
    logging.info(data.decode('latin-1'))

    #Si se reciben datos nos muestra la IP y el mensaje recibido
    print("Recibo conexion de la IP:" + str(addr[0]) + " Puerto: " + str(addr[1]))

    #Devolvemos el mensaje de exíto al cliente
    recv_msg = "log aggregó con exito"

    cli.send(recv_msg.encode())

cli.close()

