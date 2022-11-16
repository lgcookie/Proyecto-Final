### Este observador va a guardar un groupo de callbacks y sus eventos correspondientes
class Observador():

    _observadores = {}
    def __init__(self):
        pass
    
    ### Por cada observador agregamos el evento correspondiente
    def actualizar(self, event_name, callbacks):
        self._observadores[str(event_name)] = callbacks

        
class Evento(Observador):
    def __init__(self, name, data, autodisparar = True):
        self.name = name
        self.data = data
        if autodisparar:
            self.disparar()

    ### Cuando hay un evento de interés, la función correspondiente se activa  
    def disparar(self):        
        if self.name in Observador._observadores:
            Observador._observadores[self.name](*self.data)