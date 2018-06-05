from django.shortcuts import render, redirect, get_object_or_404, render_to_response, redirect

#para hacer commit al momento de hacer transacciones
from django.db import transaction

# login para logear
from django.contrib.auth import login
# esto es para redireccionar de forma directa después de hacer login
from django.http import HttpResponseRedirect

from django.contrib import messages

# forms, modulos y modelos
from .forms import *
from .modulos import *
from .models import *

### HOME

def home(request):
	template = 'grupo4test/home.html'

	return render(request, template, {})

### USUARIO CLIENTE

def datos(request):

	form = InfoForm()
	# template a cargar
	template = 'grupo4test/datos.html'

	# si el usuario esta autenticado
	if request.user.is_authenticated:		
		# si se hace un request tipo POST (se mandó un formulario)
		if request.method == 'POST':
			# se toman los datos del form
			form = InfoForm(request.POST)
			# si es válido
			if form.is_valid():
				# si existe una empresa regitrada a nombre de este user
				# manejo de errores en caso de que una empresa ya registrada quiera re-registrarse 
				# no debiese pasar ...
				empresa = Empresa.objects.filter(autor=request.user)
				if empresa.count() > 0:
					return 'Error'
				# cuando no está registrada la cuestion
				# se crea la empresa a nombre del usuario
				# y se le crea su formulario respondido vacío
				else:
					print(request.user.id)
					# creacion de empresa
					emp = Empresa(rut = form.cleaned_data['rut_empresa'],
								  nombre = form.cleaned_data['nombre_empresa'],
								  autor = request.user,
								)
					emp.save()
					FormularioClasificacion.construir(emp)
					# creación de formulario respondido vacío

					# redirecta al formulario
					return redirect('formulario') 		
		# si no se entro con metodo post
		# cuando se entra por defecto a la pagina
		else:
			empresa = Empresa.objects.filter(autor=request.user)	
			# si se existe una empresa asociada al usuario
			# se renderisa la info en pantalla, junto con el formulario que respondió
			if empresa.count() > 0:
				empresa = Empresa.objects.get(autor=request.user)
				formulario = FormularioClasificacion.objects.get(empresa=empresa)
				respuestas = RespuestasClasificacion.objects.filter(formulario = formulario)
				return render(request, template, {'empresa' : empresa,
												  'respuestas' : respuestas,
												  'formulario': formulario })
			# si no existe la empresa se manda el formulario para que llene los datos	
			else:
				form = InfoForm()
				return render(request, template, {'form': form,
												  'not_info': 'not_info'})

	# si no está autenticado devuelve la base 
	return render(request, template, {})
	
def diagnostico(request):
	# template a cargar
	template = 'grupo4test/diagnostico.html'
	
	# en construcción . . . 
	return render(request, template, {})

def formulario(request):
	# template a cargar
	template = 'grupo4test/formulario.html'

	if request.user.is_authenticated:

		# si no registró una empresa no puede seguir, se redirecta a 'datos' 
		if Empresa.objects.filter(autor=request.user).count() == 0:
			return redirect('datos')

		# se hace una referencia a la empresa del autor
		empresa = Empresa.objects.get(autor=request.user)
		print('empresa ' + empresa.nombre)
		# si existe el formulario relacionado a esa empresa
		# se supone debiese crearse uno vacío al inscribir datos
		if FormularioClasificacion.objects.filter(empresa=empresa).count() > 0:	
			
			formulario = FormularioClasificacion.objects.get(empresa=empresa)
			print(formulario.respondido)
			#print('formulario')
			#print(FormularioClasificacion.objects.filter(empresa=empresa))
			# si el formulario fue respondido se imprime en pantalla la wea 
			
			
			if formulario.respondido:
				print('respondido')
				respuestas = RespuestasClasificacion.objects.filter(formulario=formulario).order_by('pregunta__numero_pregunta')
				# retorna
				return render(request, template, {'respuestas' : respuestas,
												  'formulario': formulario })
			
	
		# si se hace un request tipo POST => se llenó un formulario => formulario no fue respondido 
		if request.method == 'POST':
			# se pesca la data dentro del form y se lleva a un diccionario
			# la id de los fields es la id de la pregunta en PreguntaClasificacion
			# ex: data['1'] = 'Si' => respuesta para pregunta de id 1 es 'Si'
			data = request.POST.dict()
			formulario = FormularioClasificacion.objects.get(empresa=empresa)

			# se construye el formulario con las preguntas respondidas
			#QuestionForm.getInfo(data, empresa)
			FormularioClasificacion.ponerPuntaje(data, empresa)
			#FormularioClasificacion.calcularPuntaje(formulario)
			print(formulario.puntaje)
			#FormularioClasificacion.setEtapa(formulario)
			#FormularioClasificacion.ponerPuntaje(data,formulario)
			#formulario.calcularPuntaje()
			# se llama a si mismo y muestra caso donde formulario fue respondido
			return redirect('formulario')

	question_form = QuestionForm()
	return render(request, template, {'question_form': question_form})

### ADMIN

def clasificar(request, rut_empresa):
	template = 'grupo4test/clasificar.html'

	formulario = FormularioClasificacion.objects.get(empresa__rut=rut_empresa)
	respuestas = RespuestasClasificacion.objects.filter(formulario=formulario).order_by('pregunta__numero_pregunta')

	if request.method == 'POST':
		puntajes = request.POST.dict()
		print(puntajes['etapa'])
		for pregunta in PreguntaClasificacion.objects.all():
			if puntajes.get(str(pregunta.id)):
				print(pregunta.texto_pregunta + ' ' + puntajes[str(pregunta.id)])
				r = RespuestasClasificacion.objects.get(formulario=formulario, pregunta=pregunta)
				r.puntaje = puntajes[str(pregunta.id)]
				r.save()
				if puntajes.get('com_' + str(pregunta.id)) or puntajes.get('com_' + str(pregunta.id)) == '':
					r.comentario = puntajes['com_' + str(pregunta.id)]
					r.save()
			else:
				r = RespuestasClasificacion(pregunta = pregunta,
										formulario = formulario,
										puntaje=0,
										respuesta='')
				r.save()
				continue

	
		respuestas = RespuestasClasificacion.objects.filter(formulario=formulario).order_by('pregunta__numero_pregunta')
		formulario.calcularPuntaje()
		formulario.empresa.setEtapa(puntajes['etapa'])
		print('validado ' + str(puntajes.get("validado")))
		if str(puntajes.get("validado")) == 'on':
			formulario.validado = True
		else:
			print('Nope')
			formulario.validado = False
		#formulario.validado = True
		formulario.save()

	return render(request, template, {'formulario': formulario,
									  'respuestas': respuestas })


def clasificados(request):
	template = 'grupo4test/clasificados.html'

	formularios = FormularioClasificacion.objects.filter(respondido=True).order_by('validado')

	return render(request, template, {'formularios': formularios })


def diagnosticados(request):	
	template = 'grupo4test/diagnosticados.html'

	return render(request, template, {})

## REGISTRO
def register(request):

	template = 'grupo4test/register.html'

	form = CustomUserCreationForm()
	
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account created successfully')
			#render(request, "grupo4test/wea.html", {})
			#redirect('grupo4test/accounts/login/')
	
	return render(request, template, {'form': form})


# PRUEBA
def base(request):
	# Se declara el template que se usará
	template = 'grupo4test/iteracion2.html'
	
	# Se instancia un FullForm desde forms.py
	form = FullForm()

	# Si se apreta el boton
	if request.method == 'POST':
		form = FullForm(request.POST)
		if form.is_valid():
			if request.POST.get('go'):
				# Se obtiene la info del form
				cd = form.cleaned_data
				run = cd.get('run')
				nombre_empresa = cd.get('nombre_empresa')
				nombre = cd.get('nombre')
				apellido = cd.get('apellido')
				email = cd.get('email')
				url = cd.get('url')
				postulante_id = 0
 
				# new_user es para verificar si es que: 
				# - la empresa a postular es nueva
				# - ya habia postulado antes
				# - si es que ya habia postulado antes ver si coinciden los nombres de las empresa
				new_user = False
				# checkea si ya hay un registro del RUN en la base
				if not checkPostulante(run):
					new_user = True
					# Se hace el commit antes de seguir
					transaction.commit(addUser(run,nombre_empresa,nombre,apellido, email, str(url)))

				# Si es que ya existe el RUN en la base
				else:
					# Se checkea si coincide el RUN con la empresa ingresada
					if not checkRunEmpresa(run, nombre_empresa):
						respuesta = 'No coincide el RUN de la empresa ingresad con la registrada'
						return render(request, template, {'form': form,
												  'respuesta': respuesta})

				# Se instancia un Formulario con los valores restantes del form y el ID del postulante
				postulante_id = Postulante.objects.get(run=run)
				formulario = Formulario(postulante=postulante_id,
										variable_hid = cd.get('hid_field'),
										variable1=cd.get('var1'),
										variable2=cd.get('var2'),
										variable3=cd.get('var3'),
										result=0)
				# Se llama el método que calcula el resultado del formulario y se guarda
				formulario.setResult()
				formulario.save()

				# Si el usuario es nuevo o ya existia hace variar la respuesta en el html
				if new_user:
					respuesta = 'Se inscribió nueva empresa: ' + nombre_empresa + ' a nombre de ' + nombre + ' ' + apellido + '.'
				else:
					respuesta = 'Empresa ' + nombre_empresa + ' ya estaba a nombre de ' + nombre + ' ' + apellido
				resultado = 'Puntaje: ' + str(formulario.result) + '.'
				# Se limpia el form
				form = FullForm()
				# Se retorna la nueva página
				return render(request, template, {'form': form,
												  'respuesta': respuesta,
												  'resultado': resultado})
	# Se retorna el primer ingreso a la página, con solo el form vacío
	return render(request, template , {'form': form })