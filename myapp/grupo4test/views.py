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
from .models import *

### HOME

def home(request):
	template = 'grupo4test/home.html'

	return render(request, template, {})

### USUARIO CLIENTE

def ejemplo(request):

	template = 'grupo4test/ejemplo.html'

	if request.method == 'POST':
		form = ejemploForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			print(cd.get('Nombre'))
			print(cd.get('Apellido'))

	form = ejemploForm()
	return render(request, template, {'form':form })


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

def clasificar(request, 
	):
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

