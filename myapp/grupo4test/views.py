from django.shortcuts import render, redirect, get_object_or_404, render_to_response, redirect

#para hacer commit al momento de hacer transacciones
from django.db import transaction

# para subir archivos
from django.core.files.storage import FileSystemStorage

# login para logear
from django.contrib.auth import login as auth_login, authenticate
# esto es para redireccionar de forma directa después de hacer login
from django.http import HttpResponseRedirect

from django.contrib import messages

#para crear objeto user
from django.contrib.auth.models import User

# forms, modulos y modelos
from .forms import *
from .models import *

import os

from django.conf import settings

from django.views import View

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

aux_dict = {}

### HOME

def home(request):
	template = 'grupo4test/home.html'

	if not request.user.is_authenticated:
		print('no estay') 
		return redirect('login')

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

	# template a cargar
	template = 'grupo4test/datos.html'

	# si el usuario esta autenticado
	if request.user.is_authenticated:		
		# si se hace un request tipo POST (se mandó un formulario)

		cliente = Cliente.objects.get(user=request.user)

		return render(request, template, {'cliente': cliente})

		"""
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
					FormularioClasificacion.construir(empresa[0])
					FormDiagnostico.construir(empresa[0])
					return redirect("formulario")
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
					FormDiagnostico.construir(emp)
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
	"""
	# si no está autenticado devuelve la base 
	return render(request, template, {})
	
def diagnostico(request):
	# template a cargar
	template = 'grupo4test/diagnostico.html'

	if request.user.is_authenticated:
		# Debe registrar la empresa si no no puede hacer el formulario
		cliente = Cliente.objects.get(user=request.user) 
		formulario = FormDiagnostico.objects.get(cliente=cliente)
		
		if request.method == 'POST':
			for item in request.POST:
					try:
						pregunta = PreguntaDiagnostico.objects.filter(id=item)
					except:
						print('error al tratar de buscar por ' + str(item))
						continue
					if pregunta.count() > 0:
						pregunta = pregunta[0]
						#print(pregunta.getTipo())
						# respuestas de preguntas tipo 'ALTERNATIVA'
						if pregunta.getTipo() == 'a':
							respuesta = RespuestaDiagnostico.objects.filter(pregunta=pregunta, formulario=formulario)
							r = TipoAlternativa.objects.get(id=request.POST.dict()[item])
							#print(r)
							if respuesta.count() > 0:
								print('TipoAlternativa Ya existe, se le pondrá :')
								print(r.texto_alternativa)
								print(r.puntaje)
								respuesta = respuesta[0]
								respuesta.respuesta_alternativa = r
								respuesta.respuesta = r.texto_alternativa
								respuesta.puntaje = r.puntaje
								respuesta.save()
							else:
								print('TipoAlternativa no existe')
								print('Creando . . . ')
								respuesta = RespuestaDiagnostico(
											formulario = formulario,
											pregunta = pregunta,
											respuesta = r.texto_alternativa,
											puntaje = r.puntaje,
											)
								respuesta.save()
						# respuestas de preguntas tipo 'ELECCIÓN'
						elif pregunta.getTipo() == 'e':
							respuesta = RespuestaDiagnostico.objects.filter(pregunta=pregunta, formulario=formulario)
							r = TipoElegir.objects.filter(id__in=request.POST.getlist(item))
							puntaje = 0
							for res in r:
								puntaje = puntaje + res.puntaje
							if respuesta.count() > 0:
								respuesta = respuesta[0]
								respuesta.respuestas_eleccion.set(r)
								respuesta.puntaje = puntaje
								respuesta.save()
							print(r)
			if request.POST.get('guardar'):
				print('Guardar!')
				#end for
				tiempo = Tiempos()
				tiempo.save()
				formulario.guardados.add(tiempo)
				formulario.ponerPuntaje()
				tiempo.save()

			elif request.POST.get('enviar'):
				import datetime
				formulario.ponerPuntaje()
				formulario.fecha_termino = datetime.datetime.now()
				formulario.respondido = True
				formulario.save()
			#cliente = Cliente.objects.get(user=request.user)
			#formulario = FormDiagnostico.objects.get(cliente=cliente)

			#print(request.POST.dict())

						#print(request.POST.getlist(item))
						
						#respuesta = RespuestaDiagnostico.objects.filter(pregunta=pregunta, formulario=formulario)


		formularios = []

		for i in range(5):
			formularios.append(DiagForm(i+1,formulario))

		return render(request, template, {'formularios': formularios,
										  'formulario': formulario})


		"""
		empresa = Empresa.objects.get(autor=request.user)
		formulario = FormDiagnostico.objects.get(empresa=empresa)

		if request.method == 'POST':

			if request.FILES is not None:
				for file in request.FILES:
					#print(file)

					#print(myfile)
					#name, ext = os.path.splitext(str(request.FILES[file]))
					#print('extension :' +  str(ext)[1:])
					extension = str(os.path.splitext(str(request.FILES[file]))[1])[1:]
					documento = Document(empresa=empresa, document=request.FILES[file], extension=extension)
					documento.save()   
					print('Extensión del documento: ' + documento.extension)
					formulario.addFile(documento, file)
					
			# se pesca la data dentro del form y se lleva a un diccionario
			# la id de los fields es la id de la pregunta en PreguntaClasificacion
			# ex: data['1'] = 'Si' => respuesta para pregunta de id 1 es 'Si'
			

			data = request.POST.dict()
			formulario.responder(data)
			formulario.respondido = True
			formulario.save()

			# se construye el formulario con las preguntas respondidas
			#QuestionForm.getInfo(data, empresa)
			#FormDiagnostico.ponerPuntaje(data, empresa)
			#FormularioClasificacion.calcularPuntaje(formulario)
			#print(formulario.puntaje)
			#FormularioClasificacion.setEtapa(formulario)
			#FormularioClasificacion.ponerPuntaje(data,formulario)
			#formulario.calcularPuntaje()
			# se llama a si mismo y muestra caso donde formulario fue respondido
			#return redirect('formulario')

		if FormDiagnostico.objects.filter(empresa=empresa).count() > 0:

			if not FormularioClasificacion.objects.get(empresa=empresa).validado:
				return render(request, template, {'error': 'No tienes etapa todavía, no puedes hacer este formulario.'})

			formulario = FormDiagnostico.objects.get(empresa=empresa)
			# Se crea una donde se insertarán los forms para cada Q
			forms = []

			print("Q " + str(formulario.Q))
			for i in range(1,formulario.Q+2):
				#Por cada Q se crea un DiagForm correspondiente a ese Q y se guarda en la lista
				forms.append(DiagForm(i,formulario))				

			# Se le manda la lista entera al template, después imprime los Q{n} en cada tab
			return render(request, template, {'forms': forms,
											  'formulario': formulario})

	"""
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

def clasificar(request,rut_empresa):
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
		FormDiagnostico.actualizar(formulario.empresa)
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

	formularios = FormDiagnostico.objects.filter(respondido = True).order_by('estado')

	return render(request, template, {'formularios': formularios})








def diagnosticar(request,rut_empresa):
	template = 'grupo4test/diagnosticar.html'

	cliente = Cliente.objects.get(user=request.user)
	formulario = FormDiagnostico.objects.get(cliente=cliente)
	#respuestas = RespuestaDiagnostico.objects.filter(formulario=formulario).exclude(respuesta='').order_by('pregunta__Q','pregunta__numero','pregunta__sub_numero')

	if request.method == 'POST':
		puntajes = request.POST.dict()
		print(puntajes)
		#print(puntajes['etapa'])
		Q = list(range(1,formulario.Q+2))
		print(Q)
		for pregunta in PreguntaDiagnostico.objects.filter(Q__in=Q):
			if puntajes.get(str(pregunta.id)):
				print('existe la pregunta')
				print(pregunta.texto_pregunta + ' ' + puntajes[str(pregunta.id)])
				r = RespuestaDiagnostico.objects.get(formulario=formulario, pregunta=pregunta)
				r.puntaje = puntajes[str(pregunta.id)]
				r.save()
				if puntajes.get('com_' + str(pregunta.id)) or puntajes.get('com_' + str(pregunta.id)) == '':
					r.comentario = puntajes['com_' + str(pregunta.id)]
					r.save()

		#
		#respuestas = RespuestaDiagnostico.objects.filter(formulario=formulario).order_by('pregunta__Q','pregunta__numero','pregunta__sub_numero').exclude(respuesta='')


		print(puntajes['estado'])

		#formulario.calcularPuntaje()
		#formulario.validado = True
		formulario.estado = puntajes['estado']
		formulario.save()

	respuestas = []
	for i in range(1, formulario.Q+2):
		respuesta = []
		for res in RespuestaDiagnostico.objects.filter(formulario=formulario, pregunta__Q = i).order_by('pregunta__Q','pregunta__numero','pregunta__sub_numero'):
			if res.pregunta.tipo_pregunta == 'd':
				respuesta.append(res)
				continue
			if res.respuesta == '':
				continue
			respuesta.append(res)

		respuestas.append(respuesta)
	

	"""
	for i in range(1, formulario.Q+2):
			respuestas.append(RespuestaDiagnostico.objects.filter(formulario=formulario, pregunta__Q = i).order_by('pregunta__Q','pregunta__numero','pregunta__sub_numero').exclude(respuesta=''))
	"""
	estadoForm = SetEstadoForm(formulario.estado)

	return render(request, template, {'formulario': formulario,
									  'respuestas': respuestas,
									  'estadoForm': estadoForm })

## REGISTRO
## para modificarlo se pueden cambiar las forms o views de registro
def register(request):

	template = 'grupo4test/register.html'


	initial={'username': request.session.get('username', None),
		 'email':request.session.get('email', None)}
	form = CustomUserCreationForm(request.POST or None, initial=initial)
	
	if request.method == 'POST':
		if form.is_valid():
			request.session['username'] = form.cleaned_data['username']
			request.session['email'] = form.cleaned_data['email']
			request.session['password1'] = form.cleaned_data['password1']
			return redirect('register2')

	
	return render(request, template, {'registerForm': registerForm,
									  'clasificacionForm': clasificacionForm })

def register2(request):
	template = 'grupo4test/register2.html'
	initial = {'rut_empresa':request.session.get('rut_empresa'),
		'nombre_empresa': request.session.get('nombre_empresa'),
		'desc_empresa': request.session.get('desc_empresa'),
		'equipo_empresa': request.session.get('equipo_empresa'),
		'ventas_empresa': request.session.get('ventas_empresa')
		}
	form = RegistrationForm(request.POST or None, initial=initial)

	if request.method == 'POST':
		if form.is_valid():
			request.session['rut_empresa'] = form.cleaned_data['rut_empresa']
			request.session['nombre_empresa'] = form.cleaned_data['nombre_empresa']
			request.session['desc_empresa'] = form.cleaned_data['desc_empresa']
			request.session['equipo_empresa'] = form.cleaned_data['equipo_empresa']
			request.session['ventas_empresa'] = form.cleaned_data['ventas_empresa']
			ventas = request.session['ventas_empresa']
			print(ventas)
			if ventas == '0':
				#construir objetos y postear IDEA
				username = request.session['username']
				email = request.session['email']
				password = request.session['password1']
				user = User.objects.create_user(username,email,password)

				rut = request.session['rut_empresa']
				nom = request.session['nombre_empresa']
				desc = request.session['desc_empresa']
				equip = request.session['equipo_empresa']

				empresa = Empresa.objects.create(rut=rut, nombre=nom, etapa='Idea',autor=user)
				FormDiagnostico.construir(empresa)
				messages.success(request, 'Registro completado')
				request.session.clear()
				return redirect('register')
			else:
				return redirect('register3')
		else:
			print("forma no valida")

	return render(request, template, {'form':form})

def register3(request):
	template = 'grupo4test/register3.html'
	ventas = request.session['ventas_empresa']
	print(ventas)
	if ventas == '1':
		initial={'ded_equipo': request.session.get('ded_equipo'),
				'feedback': request.session.get('feedback')}
		form = RegistrationForm2(request.POST or None, initial=initial)
		if request.method == 'POST':
			if form.is_valid():
				request.session['ded_equipo'] = form.cleaned_data['ded_equipo']
				request.session['feedback'] = form.cleaned_data['feedback']
				#filtro
				if request.session['ded_equipo'] and request.session['feedback']:
					etapa='Semilla'
				else:
					etapa='Idea'
				##crear objeto y guardar
				#form.save()
	else:
		initial={'mvp': request.session.get('mvp'),
			'plan_exp': request.session.get('plan_exp'),
			'fig_legal': request.session.get('fig_legal'),
			'ventas_ext': request.session.get('ventas_ext'),
			'fin_priv': request.session.get('fin_priv'),
			'plan_inter': request.session.get('plan_inter'),
			'vida_emp': request.session.get('vida_emp'),
			'mod_ext': request.session.get('mod_ext'),
			'est_inter': request.session.get('est_inter')}
		form =RegistrationForm3(request.POST or None, initial=initial)
		if request.method == 'POST':
			if form.is_valid():
				request.session['mvp'] = form.cleaned_data['mvp']
				request.session['plan_exp'] = form.cleaned_data['plan_exp']
				request.session['fig_legal'] = form.cleaned_data['fig_legal']
				request.session['ventas_ext'] = form.cleaned_data['ventas_ext']
				request.session['fin_priv'] = form.cleaned_data['fin_priv']
				request.session['plan_inter'] = form.cleaned_data['plan_inter']
				request.session['vida_emp'] = form.cleaned_data['vida_emp']
				request.session['mod_ext'] = form.cleaned_data['mod_ext']
				request.session['est_inter'] = form.cleaned_data['est_inter']

				mvp = request.session['mvp']
				plan_exp = request.session['plan_exp']
				fig_legal = request.session['fig_legal']
				ventas_ext = request.session['ventas_ext']
				fin_priv = request.session['fin_priv']
				plan_inter = request.session['plan_inter']
				vida_emp = request.session['vida_emp']
				mod_ext = request.session['mod_ext']
				est_inter = request.session['est_inter']

				temprana = mvp and plan_exp
				expansion = temprana and ventas_ext and fin_priv and plan_inter
				internac = expansion and vida_emp and mod_ext and est_inter

				if internac:
					print("internacionalizacion")
					etapa = 'Internacionalización'
				elif expansion:
					print("expansion")
					etapa = 'Expansión'
				elif temprana:
					print("ET")
					etapa = 'Etapa Temprana'
				else:
					print("Semilla")
					etapa = 'Semilla'
				#form.save()

	if request.method == 'POST':
		username = request.session['username']
		email = request.session['email']
		password = request.session['password1']
		user = User.objects.create_user(username,email,password)

		rut = request.session['rut_empresa']
		nom = request.session['nombre_empresa']
		desc = request.session['desc_empresa']
		equip = request.session['equipo_empresa']

		empresa = Empresa.objects.create(rut=rut, nombre=nom, etapa=etapa,autor=user)
		FormDiagnostico.construir(empresa)
		messages.success(request, 'Registro completado')
		request.session.clear()
		return redirect('register')

	return render(request, template, {'form':form})

def save(request):

	template = 'grupo4test/save.html'

	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		name = os.path.splitext(str(request.FILES['myfile']))[0]
		extension = os.path.splitext(str(request.FILES['myfile']))[1]

		dbx = dropbox.Dropbox('fJeqs6wRPWAAAAAAAAAACPERxFOlBNsWhSw-4LXig1nfvVwdVqgZ3HryiyHzeCCf')

		dbx.files_upload(myfile.read(),'/ID_TEST_USER/'+name+extension,mute =True)

		print ("Archivo RECIBIDO")
		
		return render (request, template, {})

	return render(request, template, {})

def login(request):

	template = 'registration/login.html'

	form = LoginForm()

	if request.session.get('cliente'):
		cliente = Cliente.objects.get(id=request.session.get('cliente'))
		del request.session['cliente']
		return render(request, template, {'form': form, 
										  'cliente': cliente})

		
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			
			user = authenticate(request, username=user, password=password)
			if user is not None:
				auth_login(request, user)
				return redirect('home')
			else:
				return render(request, template, {'form':form, 
												  'error': 'usuario no encontrado'})

	return render(request, template, {'form': form})
		
#clase para generar pdf
class Pdf(View):

	def get(self, request, id_cliente):
		template = get_template('grupo4test/pdf.html')
		cliente = Cliente.objects.get(id=id_cliente)
		formulario = FormDiagnostico.objects.get(cliente=cliente)
		params = {
			'formulario': formulario,
		}
		html = template.render(params)
		response = BytesIO()
		pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

		if not pdf.err:
			return HttpResponse(response.getvalue(), content_type='application/pdf')
		else:
			return HttpResponse("Error Rendering PDF", status=400)