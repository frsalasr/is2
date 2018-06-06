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

``` bash
myapp/
  |-manage.py
  |-grupo4test/
```
 
En myapp/grupo4test se encuentra el programa.

Archivos y carpetas relevantes:
```
myapp/grupo4test/
  |-statics/ 
  |-templates/
  |-urls.py  
  |-views.py  
  |-models.py
```
 
## urls.py
Acá se definen las urls definidas para nuestra aplicación en Django.

Tiene la siguiente estructura:
``` python
path('path/to/.../url'/, views.'nombre vista', name='nombre referencial'),
```
Donde:
'path/to/.../url' es la dirección a la que hay que entrar para ingresar a esta página.
views.'nombre vista' es el nombre de la vista definda en views.py la cual será llamada al entrar a la url.

Ejemplo, para la url del formulario del cliente se tiene:

### Url del cliente:
    path('formulario/',views.formulario, name='formulario'),

Esto dice que si se entra a grupo4test/formulario/ va a llamar a la vista formulario.

## views.py y templates
Conjunto de vistas, cada vista tiene la siguiente estructura:

``` python
def vista1(request):
  . . .
  . . .
  . . .
  return render(request, template, {diccionario})
```

Como se definió, una url está asociada a una vista. Al momento de ingresar una url, 
el programa llamará a la vista asociada, la vista hará el proceso lógico a partir del request con la que fue llamada (el request va a variar si es que se entró como cliente o admin, si es que se entró directo a la página o fue redireccionado hacia ella, si es que se envió un formulario, etc), luego retornará un render (puede retornar muchas coasas pero nosotros usaremos render el 99% de las veces). El render tiene el request con el que fue llamado la vista, un template en html asociado y un diccionario, un diccionario en python es de la forma: 
```python
{ 'key1' : value1 , 'key2': value2 }
```
El diccionario "envía" variables desde la parte lógica de la vista al template de html.

El template es la página en sí, está escrito en html y toma las variables enviadas desde la vista para crear la página.

Las variables enviadas desde el diccionario pueden ser de la forma: 
```
{{ variable }} 
```
Se puede iterar y hacer condicionales dentro del template, usando:
```
{% if condicional %}
< do something > 
{% else %}
< do something >
{% endif %}
. 
. 
.
{% for element in list %}
< do something >
{% endfor %}
```
Por ejemplo, si en la vista, el diccionario enviado tiene la forma: 
```python
{'error':'no se encontró el usuario'}
```
Al principio del template de html se puede poner:
```python
{% if error %}
<p>{{ error }}</p>
{% endif %}
```
Por lo que imprimirá el error.

Ejemplo (muy resumido):

```python
def formulario(request):
	template = 'grupo4test/formulario.html'
	question_form = QuestionForm()
return render(request, template, {'question_form': question_form})
```

Si se entra a grupo4test/formulario se llama esta vista.
Esta vista crea una instancia de QuestionForm y se la envía al template que se encuentra en grupo4test/formulario.html.

En el template.html se tiene 

```html
<form method="post">
	{% csrf_token %}
	{% for field in question_form %}
		<p>{{ field.label }}</p>
		<p>{{ field }}</p>
	{% endfor %}
	<input type="submit" name="submit" value="Enviar" />
</form>
```

Creará un form que tome el método post.
Por cada campo dentro del QuestionForm instanciado en la vista que fue enviado como question_form imprimirá el label del campo y el campo.
Una vez terminado el bucle pondrá el botón de submit.




  
  




