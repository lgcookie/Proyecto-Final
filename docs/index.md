# Proyecto Final 
``` {warning}
Este proyecto todavía es de bajo desarrollo pesado
```

## Proyecto Descripción
La idea fundamental detrás mi proyecto es para crear una Tkinter aplicación en la cual usaré para manejar la administración de cuentas en un otro sitio web. Solomente dando acceso a usarios quienes hayan recibido un código de verificación. Es posible que el usuario pueda registrar en cuenta al través el sitio o podría manejadore de usarios. En el futuro voy a vincular esta siestma con el baso de datos en vivo, y también agregar un correo manejador para mandar los codígos de verificación.

## Comienza Rapido
```{code-block}
$ git clone https://github.com/lgcookie/flask_app.git
$ pip install -r requisitos.txt
$ python3 controler.py
```

## Tabla de Objetivos
| Objetivos | Descripción |
| ------ | --- |
| 1. | Un validator para asegurar que el usuario ya no existe en el baso de datos, y avisar el usario si no |
| 2. | Un validator para asegurar que el correo sigue un format standard, y avisar el usario si no  |
| 3. | Un validator para asegurar que el nombre de la empresa sigue un format standard, y avisar el usario si no |
| 4. | Un opción que permite añadir un usuario con o sin un codígo de verificación, y funcionalidad que puede generar un codígo a una fecha más tarde |
| 5. | Un observador que se activa después ciertos eventos. Al medidante el uso de evento oyentes el observador va a ejecutar los operaciones en la base de datos.  |
| 6. | Un decorador que actualiza la tabla cada vez hay un cambio en la base de datos y cuando la aplicación se inicia por la primera vez.   |
| 7. | Un decorador que maneja los logs de la applición, además de asegura que los logs que vienen de todas funciónes siguen el mismo format  |
| 8. | Un cliente-servidor conexión que envia los logs de la applición, cuando llegan al servidor, el servidor los pone en un archivo separador, el usuario también puede elegir esta herramiento o no  |

## Información adicional
Para hacer cosas mas seguro:
- La aplicación no usará el base de datos produción
- En vez un base de datos local usará
- Así que esto evitará la necesidad de compartir información de conexión a través un .env archivo. 


