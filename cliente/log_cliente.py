#Se importa el módulo
import socket

class ClienteLogger():

    # Este atributo va a cambiar cuando el usuario empuje el buton
    log_servidor = False

    def cliente_logger(self, msg):
        
        if self.log_servidor:
            #instanciamos un objeto para trabajar con el socket
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((socket.gethostname(), 9000))
            try:
                cliente_socket.send(msg.encode("latin-1"))
            except ConnectionResetError as e:
                print("not logging errors in server")
            except Exception as e:
                print(e)
            
            # Recibir el mensaje vuelta 
            cliente_socket.recv(1024).decode()
            
            # Cerrar la conexión
            cliente_socket.close()


