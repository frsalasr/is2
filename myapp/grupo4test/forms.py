from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.template.defaulttags import register

import os

################################

@register.filter
def getQ(Q):
	if Q == 1:
		return 'Modelo Negocio'
	elif Q == 2:
		return 'Gestión Organizacional'
	elif Q == 3:
		return 'Gestión Comercial'
	elif Q == 4:
		return 'Gestión Financiera'
	else:
		return 'Gestión de Innovación'

@register.filter
def setListo(cliente):
	formulario = FormDiagnostico.objects.get(cliente=cliente)
	formulario.estado = 'LISTO'
	formulario.save()
	return ""

@register.filter
def getComentario(id_question, formulario):
	if id_question.startswith('id_'):
		id_question = id_question[3:]
	r = RespuestaDiagnostico.objects.get(pregunta__id=id_question, formulario=formulario).comentario
	
	if r == '':
		return False

	return RespuestaDiagnostico.objects.get(pregunta__id=id_question, formulario=formulario).comentario

@register.filter
def getTipoA(id):
	return TipoAlternativa.objects.get(id=id)

@register.filter
def getFormularioEstado(cliente):
	return FormDiagnostico.objects.get(cliente=cliente).estado

@register.filter
def getFilename(path,op):
	return os.path.basename(path)

@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def document_exist(id_question, formulario):
	print('Revisando si existe un documento ' + str(id_question) + ' de ' + str(formulario.empresa))
	if id_question.startswith('id_'):
		id_question = id_question[3:]
	if RespuestaDiagnostico.objects.get(pregunta=id_question,formulario=formulario).documento:
		print('Existe el documento: ' + str(RespuestaDiagnostico.objects.get(pregunta=id_question,formulario=formulario).documento))
		return True
	print('No tiene documento . . . ')
	return False

@register.filter
def get_path_doc(id_question, formulario):
	if id_question.startswith('id_'):
		id_question = id_question[3:]
	documento = RespuestaDiagnostico.objects.get(pregunta=id_question,formulario=formulario).documento
	path = documento.document
	extension = documento.extension
	filename = os.path.basename(str(documento.document))
	return [path, extension, filename]

@register.filter
def get_item(diccionario, key):
	#print(diccionario)
	#print(key)
	return diccionario.get(key)

@register.filter
def get_hijo(pregunta, formulario):
	return RespuestasClasificacion.objects.get(pregunta=pregunta, formulario=formulario)

class LoginForm(forms.Form):
	username = forms.CharField(label='Usuario', required=True)
	password = forms.CharField(label='Contraseña' ,required=True, widget=forms.PasswordInput)



class HijoForm(forms.Form):
	def __init__(self):
		# Se inicia el super Form
		super(HijoForm, self).__init__()

	def crearField(self, key, tipo, label, queryset):
		self.fields[key] = createField(tipo,label,queryset)

class SetEstadoForm(forms.Form):


	def __init__(self,estado,**kwargs):
		super(SetEstadoForm, self).__init__(**kwargs)

		self.ESTADO_CHOICES = (
			('RESUELTO','RESUELTO'),
			('PENDIENTE','PENDIENTE'),
			('CORREGIR','CORREGIR'),
			)
		self.estado = estado
		self.fields['estado'] = forms.ChoiceField(label='Estado del diagnostico', choices=self.ESTADO_CHOICES, initial = self.estado)
	
def createField(tipo, label, queryset=None, initial=""):
	if tipo == 'a':
		return forms.ModelChoiceField(label=label, queryset=queryset, required=False,
									  initial=initial,
									  widget=forms.RadioSelect(),
									  empty_label=None)
	elif tipo == 'e':
		return forms.ModelMultipleChoiceField(label=label, 
											  required=False, 
											  widget=forms.CheckboxSelectMultiple,
                                        	  queryset=queryset,
                                        	  initial=initial,
                                        	 )
	
	## NO SIRVEN
	elif tipo == 't':
		return forms.CharField(label=label, required=False, initial=initial, widget=forms.Textarea(attrs={
					        																			'cols': 200,
																								        'rows': 3,
																								        'style': 'width: 50%'
																								    }))
	elif tipo == 'n':
		return forms.IntegerField(label=label, required=False, initial=initial)
	elif tipo == 'd':
		return forms.FileField(label=label, required=False)

	else:
		return 'error'

class DiagForm(forms.Form):
	#hidden = forms.IntegerField()

	def __init__(self,dimension,formulario,**kwargs):
		# Se inicia el super Form
		super(DiagForm, self).__init__(**kwargs)

		
		self.formulario = formulario
		self.dimension = dimension
		# se guardan los forms hijos
		self.base = {}
		self.papa = {}
		#self.doc = {}
		etapa = Etapa.objects.get(etapa=self.formulario.cliente.etapa)
		#print('etapa ' + str(self.formulario.cliente.etapa))
		# busca las preguntas 
		for pregunta in PreguntaDiagnostico.objects.filter(pregunta_base=True, etapas__in=[etapa], dimension=self.dimension).order_by('numero'):
			#print(pregunta)
			pregunta_key = str(pregunta.id)
			self.base['id_' + pregunta_key] = 1

			respuesta = RespuestaDiagnostico.objects.filter(pregunta=pregunta, formulario=formulario)
			# existe la respuesta (como instancia)
			if respuesta.count() > 0:
				respuesta = respuesta[0]
				if pregunta.getTipo() == 'a':
					if respuesta.respuesta_alternativa:
						#print('respuesta alternativa' + str(respuesta.respuesta_alternativa))
						self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_alternativa.all(), respuesta.respuesta_alternativa)
					else:
						self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_alternativa.all())

				elif pregunta.getTipo() == 'e':
					if respuesta.respuestas_eleccion:
						print('yup, existen las respuestas')
						print(respuesta)
						print(respuesta.respuestas_eleccion.all())
						self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_eleccion.all(), respuesta.respuestas_eleccion.all())
					
					else:
						self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_eleccion.all())
			# si no existe RespuestaAlternativa todavía
			else:
				if pregunta.getTipo() == 'a':
					self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_alternativa.all())
				elif pregunta.getTipo() == 'e':
					self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_eleccion.all())



			preguntas_hijas = PreguntaDiagnostico.objects.filter(depende_de=pregunta).order_by('sub_numero')
			if preguntas_hijas.count() > 0:
				for question in preguntas_hijas:
					print(question)
					self.papa['id_' + str(question.id)] = "id_" + pregunta_key

					respuesta = RespuestaDiagnostico.objects.filter(pregunta=question, formulario=formulario)
					if respuesta.count() > 0:
						respuesta = respuesta[0]
						if question.getTipo() == 'a':
							respuesta = RespuestaDiagnostico.objects.get(pregunta=question, formulario=formulario)
							if respuesta.respuesta_alternativa:
								#print('respuesta alternativa' + str(respuesta.respuesta_alternativa))
								self.fields[question.id] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all(), respuesta.respuesta_alternativa)
							else:
								self.fields[question.id] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all())
						elif question.getTipo() == 'e':
							respuesta = RespuestaDiagnostico.objects.get(pregunta=pregunta, formulario=formulario)
							if respuesta.respuestas_eleccion:
								print('yup, existen las respuestas')
								print(respuesta)
								print(respuesta.respuestas_eleccion.all())
								self.fields[question.id] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_eleccion.all(), respuesta.respuestas_eleccion.all())
							else:
								self.fields[question.id] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_eleccion.all())
					else:
						if pregunta.getTipo() == 'a':
							self.fields[question.id] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all())
						elif pregunta.getTipo() == 'e':
							self.fields[question.id] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_eleccion.all())

		# Se llama a todas las preguntas de clasificación 
		# Por cada pregunta de clasificación

		"""

		for pregunta in PreguntaDiagnostico.objects.filter(pregunta_base=True, etapas__in=[self.etapa]).order_by('numero'):
			# self.fields[key] es un diccionario key -> form 
			# Ejemplo para pregunta tipo respuesta en texto
			# self.field['pregunta_n'] = forms.CharField(required = False)
			# Después el view instancia el field del form 
			# para referirse a el basta con QuestionForm.cleaned_data['pregunta_n']
			# Se define la Key del diccionario como pregunta_(id_pregunta), ex: pregunta_1, pregunta_20, etc
			pregunta_key = str(pregunta.id)
			self.base['id_' + pregunta_key] = 1
			print(str(pregunta.id) + ' ' + str(self.base['id_'+pregunta_key]))
			# se toman las preguntas que dependen de esta
			#if pregunta.getTipo() == 'd':
			#	print(str(pregunta.id) + ' es documento')
			#	self.doc['id_' + pregunta_key] = 1

			respuesta = RespuestaDiagnostico.objects.get(pregunta = pregunta, formulario = formulario)
			#print(respuesta)

			self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_alternativa.all(), respuesta.respuesta)
			# Se guarda la pregunta para presentarla en el form

			
			preguntas_hijas = PreguntaDiagnostico.objects.filter(depende_de=pregunta).order_by('sub_numero')
			if preguntas_hijas.count() > 0:
				for question in preguntas_hijas:
					answer = RespuestaDiagnostico.objects.get(pregunta = question, formulario = formulario)
					self.papa['id_' + str(question.id)] = "id_" + pregunta_key
					#if question.getTipo() == 'd':
						#print(str(question.id) + ' es documento')
						#self.doc['id_' + str(question.id)] = 1
					self.fields[str(question.id)] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all(), answer.respuesta)
		"""
# Form que toma TODAS las preguntas para clasificar y dependiendo del tipo de esta crea un field
class QuestionForm(forms.Form):
	#hidden = forms.IntegerField()

	def __init__(self):
		# Se inicia el super Form
		super(QuestionForm, self).__init__()
		
		
		# se guardan los forms hijos
		self.base = {}
		self.papa = {}

		# Se llama a todas las preguntas de clasificación 
		# Por cada pregunta de clasificación


		for pregunta in PreguntaClasificacion.objects.filter(pregunta_base=True).order_by('numero'):
			# self.fields[key] es un diccionario key -> form 
			# Ejemplo para pregunta tipo respuesta en texto
			# self.field['pregunta_n'] = forms.CharField(required = False)
			# Después el view instancia el field del form 
			# para referirse a el basta con QuestionForm.cleaned_data['pregunta_n']
			# Se define la Key del diccionario como pregunta_(id_pregunta), ex: pregunta_1, pregunta_20, etc
			pregunta_key = str(pregunta.id)
			self.base['id_' + pregunta_key] = 1
			# se toman las preguntas que dependen de estaa 

			self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_alternativa.all())
			# Se guarda la pregunta para presentarla en el form
			#self.preguntas.append(pregunta.texto_pregunta)
			
			preguntas_hijas = PreguntaClasificacion.objects.filter(depende_de=pregunta)
			if preguntas_hijas.count() > 0:
				for question in preguntas_hijas:
					self.papa['id_' + str(question.id)] = "id_" + pregunta_key
					self.fields[str(question.id)] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all())


	def ponerPuntaje(self, respuestas, cliente):
		puntaje = 0
		for pregunta in PreguntaClasificacion.objects.all():
			if respuestas.get(str(pregunta.id)):
				#print('llegué')
				respuesta = TipoAlternativa.objects.get(id=respuestas.get(str(pregunta.id)))
				puntaje = puntaje + (pregunta.ponderacion*respuesta.puntaje)*5

		#print(puntaje)
		etapa = self.definirEtapa(puntaje)
		print('Cambiando estado del cliente ' + str(cliente) + ' a ' + etapa)
		cliente.etapa = self.definirEtapa(puntaje)
		cliente.save()
		return puntaje
		#print(self.definirEtapa(puntaje))

	def definirEtapa(self, puntaje):
		if puntaje <= 3:
			return 'Idea'
		elif puntaje > 3 and puntaje <= 6:
			return 'Semilla'
		elif puntaje > 6 and puntaje <= 9:
			return 'Etapa Temprana'
		elif puntaje > 9 and puntaje <= 12:
			return 'Expansión'
		else:
			return 'Internacionalización'


	"""
	def getInfo(data, empresa):

		if FormularioClasificacion.objects.filter(empresa=empresa).count() > 0:
			#print('ya existe!')
			#print(FormularioClasificacion.objects.filter(empresa=empresa))
			FormularioClasificacion.construir(empresa)
			#print(FormularioClasificacion.objects.filter(empresa=empresa))

		formulario = FormularioClasificacion(empresa=empresa, puntaje=0)
		formulario.save() 

		for pregunta in PreguntaClasificacion.objects.all():
			if data.get(str(pregunta.id)):
				print(pregunta.texto_pregunta)
				respuesta = TipoAlternativa.objects.get(id=data.get(str(pregunta.id))).puntaje 
				print(respuesta)
				r1 = RespuestasClasificacion.objects.get(pregunta=pregunta, formulario=formulario)
				r1.puntaje = respuesta
				r1.save()	

	
	def getCleaned(self, empresa):

		if FormularioClasificacion.objects.filter(empresa=empresa).count() > 0:
			print('ya existe!')
			FormularioClasificacion.objects.filter(empresa=empresa).delete()

		formulario = FormularioClasificacion(empresa=empresa, puntaje=0)
		formulario.save()

		for pregunta in PreguntaClasificacion.objects.filter(base_question=True).order_by('numero_pregunta'):
			respuesta = self.cleaned_data[pregunta.id]
			r = RespuestaClasificacion(pregunta=pregunta, formulario=formulario, puntaje=0, respuesta=respuesta)
			r.save()
			preguntas_hijas = PreguntaClasificacion.objects.filter(depende_de=pregunta)
			if preguntas_hijas.count() > 0:
				form_hijo = self.hijos['id_' + str(pregunta.id)]
				for question in preguntas_hijas:
					respuesta = form_hijo.cleaned_data['id_' + question.id]
					r = RespuestaClasificacion(pregunta=question, formulario=formulario, puntaje=0, respuesta=respuesta)
					r.save()
		formulario.respondido = True;

	# getters
	def getPreguntas(self):
		return self.preguntas

	def getAt(self,pregunta_id):
		return self.preguntas[pregunta_id]

	"""
# Form para poner datos empresa (run y nombre)
class InfoForm(forms.Form):
	rut_empresa = forms.IntegerField(label='RUT',required=True)
	nombre_empresa = forms.CharField(label='Nombre Empresa', max_length=32, required=True)

# Form para registrar usuario
class CustomUserCreationForm(forms.Form):
	# campos

    username = forms.CharField(label='Usuario', min_length=4, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme contraseña', widget=forms.PasswordInput)
    nombre = forms.CharField(label='Nombre')
    apellido = forms.CharField(label='Apellido')
    telefono = forms.IntegerField(label='Telefono')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        # se cuentan
        r = User.objects.filter(username=username)
        # si hay > 0 entonces ya existe
        if r.count():
            raise  ValidationError("Usuario ya existe")
        return username

    # la misma mierda para el mail y las passes
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email ya registrado")
        return email

    # same
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no son las mismas")

        return password2
    
    # same
    def save(self, commit=True):
        user = User.objects.create_user(
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['nombre'],
            last_name = self.cleaned_data['apellido'],
        )
        user.save()
        cliente = Cliente(user=user,
        				  telefono= self.cleaned_data['telefono'])
        cliente.save()
        return cliente

#Formulario de registro debe incluir datos y clasificación
class RegistrationForm(forms.Form):
 	nombre_empresa = forms.CharField(label='Nombre del emprendimiento', max_length=32, required=True)
 	desc_empresa = forms.CharField(label='Descripción del emprendimiento', max_length=500, required=True, widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
 	equipo_empresa = forms.CharField(label='Descripción del equipo de trabajo', max_length=500, required=True, widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
 	ventas_empresa = forms.ChoiceField(label='Ventas en el último año', required=True, widget=forms.Select(), choices=[(0,'No hay ventas'), (1,'Menores a 2400UF'), (2,'Mayores a 2400UF')])

class RegistrationForm2(forms.Form):
	ded_equipo = forms.BooleanField(label='El equipo está dedicado al 100%', required=False)
	feedback =  forms.BooleanField(label='Han tenido feedback de Clientes', required=False)

class RegistrationForm3(forms.Form):
	mvp = forms.BooleanField(label='MVP desarrollado', required=False)
	plan_exp = forms.BooleanField(label='Plan de expansión', required=False)
	fig_legal = forms.BooleanField(label='Figura legal', required=False)
	ventas_ext = forms.BooleanField(label='Ventas en el extranjero', required=False)
	fin_priv = forms.BooleanField(label='Financiamiento privado', required=False)
	plan_inter = forms.BooleanField(label='Plan de internacionalización', required=False)
	vida_emp = forms.BooleanField(label='La empresa tiene menos de 3 años', required=False)
	mod_ext = forms.BooleanField(label='Modelo de negocio vinculado al exteror', required=False)
	est_inter = forms.BooleanField(label='Producto con estandares internacionales de diseño y producción', required=False)

##### TEST FORMS #####
# OBSOLETOS #

class FullForm(forms.Form):

	# ociones para elegir en ChoiseField cuanto_gana
	options=(
		('si', 'si'),
		('no', 'no'),
		('tal vez', 'tal vez'),
		)
	#cuanto_gana = forms.ChoiceField(choices=options, initial='no')
	

	run = forms.IntegerField()
	nombre_empresa = forms.CharField(max_length=20)
	nombre = forms.CharField(max_length=20)
	apellido = forms.CharField(max_length=20)
	email = forms.EmailField()
	url = forms.URLField(required = False)

	hid_field = forms.IntegerField(required = False)
	var1 = forms.IntegerField()
	var2 = forms.IntegerField()
	var3 = forms.IntegerField()

	def getName(self):
		return 'Pregunta 2'

class DinamicForm(forms.Form):

	run = forms.IntegerField()
	nombre_empresa = forms.CharField(max_length=20)
	nombre = forms.CharField(max_length=20)
	apellido = forms.CharField(max_length=20)
	email = forms.EmailField()

	def getName(self):
		return 'Pregunta 1'
