# is2

Como correr el programa

Requiere python3.5.2 y django 2.0.1

Para instalar Django (requiere python 3.x)
pip install django

Como correr el programa:
python3 manage.py runserver ip:puerto

Se crea en ip:puerto/grupo4test

Ejemplo: 
python3 manage.py runserver localhost:8500

entrar a
localhost:8500/grupo4test

*********************

Como funciona Django (Muy resumido):
Existen 3 capas:
Capa de los templates (interfaz de la página: html, css, js, etc)
Capa de las vistas (lógica del programa: puro python)
Capa de los modelos (datos del programa: base de datos modelada como objetos)

Una url en django esta relacionada con una vista y la vista con un template.
Las vistas se encuentran en views.py y son un método
El template se encuentra en templates/grupo4test/template.html

Estructura de la aplicación (Muy simplificada):

Distribución de archivos y carpetas:

myapp/

  |-manage.py

  |-grupo4test/

 
En myapp/grupo4test se encuentra el programa:
Archivos y carpetas relevantes:

myapp/grupo4test/

  |-statics/
  
  |-templates/
  
  |-urls.py
  
  |-views.py
  
  |-models.py
  
 
## urls.py
Acá se definen las urls definidas para nuestra aplicación en Django.

Tiene la siguiente estructura:
path('path/to/.../url'/, views.'nombre vista', name='nombre referencial'),

Donde:
'path/to/.../url' es la dirección a la que hay que entrar para ingresar a esta página.
views.'nombre vista' es el nombre de la vista definda en views.py la cual será llamada al entrar a la url.

Ejemplo, para la url del formulario del cliente se tiene:

### Url del cliente:
    path('formulario/',views.formulario, name='formulario'),

Esto dice que si se entra a grupo4test/formulario/ va a llamar a la vista formulario.

## views.py
Conjunto de vistas, cada vista tiene la siguiente estructura:

def vista1(request):
  . . .
  . . .
  . . .
  return render(request, template, {diccionario})







  
  




