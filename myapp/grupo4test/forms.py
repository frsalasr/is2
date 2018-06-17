from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.template.defaulttags import register


################################

@register.filter
def document_exist(id_question, formulario):
	print('revisando si existe la wea')
	if id_question.startswith('id_'):
		id_question = id_question[3:]
	if RespuestaDiagnostico.objects.get(pregunta=id_question,formulario=formulario).documento:
		return True
	return False

@register.filter
def get_path_doc(id_question, formulario):
	if id_question.startswith('id_'):
		id_question = id_question[3:]
	return RespuestaDiagnostico.objects.get(pregunta=id_question,formulario=formulario).documento.document

@register.filter
def get_item(diccionario, key):
	return diccionario.get(key)

@register.filter
def get_hijo(pregunta, formulario):
	return RespuestasClasificacion.objects.get(pregunta=pregunta, formulario=formulario)

class ejemploForm(forms.Form):
	options=(
		('si', 'si'),
		('no', 'no'),
		('tal vez', 'tal vez'),
		)
	macaco = forms.ChoiceField(label='¿Es ud un macaco?', choices=options)
	nombre = forms.CharField(label='Nombre')
	apellido = forms.CharField(label='Apellido')



def createField(tipo, label, queryset=None, initial=""):
	if tipo == 'a':
		return forms.ModelChoiceField(label=label, queryset=queryset, required=False, initial=initial)
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

class HijoForm(forms.Form):
	def __init__(self):
		# Se inicia el super Form
		super(HijoForm, self).__init__()

	def crearField(self, key, tipo, label, queryset):
		self.fields[key] = createField(tipo,label,queryset)

class DiagForm(forms.Form):
	#hidden = forms.IntegerField()

	def __init__(self,Q,formulario,**kwargs):
		# Se inicia el super Form
		super(DiagForm, self).__init__(**kwargs)

		self.Q = Q
		self.formulario = formulario
		self.formulario.checkFormulario()
		# se guardan los forms hijos
		self.base = {}
		self.papa = {}
		self.doc = {}

		# Se llama a todas las preguntas de clasificación 
		# Por cada pregunta de clasificación


		for pregunta in PreguntaDiagnostico.objects.filter(base_question=True, Q=self.Q).order_by('numero'):
			print('agergando mas mierdas')
			# self.fields[key] es un diccionario key -> form 
			# Ejemplo para pregunta tipo respuesta en texto
			# self.field['pregunta_n'] = forms.CharField(required = False)
			# Después el view instancia el field del form 
			# para referirse a el basta con QuestionForm.cleaned_data['pregunta_n']
			# Se define la Key del diccionario como pregunta_(id_pregunta), ex: pregunta_1, pregunta_20, etc
			pregunta_key = str(pregunta.id)
			self.base['id_' + pregunta_key] = 1
			# se toman las preguntas que dependen de estaa 
			if pregunta.getTipo() == 'd':
				self.doc['id_' + pregunta_key] = 1

			respuesta = RespuestaDiagnostico.objects.get(pregunta = pregunta, formulario = formulario)
			#print(respuesta)

			self.fields[pregunta_key] = createField(pregunta.getTipo(), pregunta.texto_pregunta, pregunta.preguntas_alternativa.all(), respuesta.respuesta)
			# Se guarda la pregunta para presentarla en el form
			#self.preguntas.append(pregunta.texto_pregunta)
			
			preguntas_hijas = PreguntaDiagnostico.objects.filter(depende_de=pregunta).order_by('sub_numero')
			if preguntas_hijas.count() > 0:
				for question in preguntas_hijas:
					answer = RespuestaDiagnostico.objects.get(pregunta = question, formulario = formulario)
					self.papa['id_' + str(question.id)] = "id_" + pregunta_key
					self.fields[str(question.id)] = createField(question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all(), answer.respuesta)

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


		for pregunta in PreguntaClasificacion.objects.filter(base_question=True).order_by('numero_pregunta'):
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

			"""
			if preguntas_hijas.count() > 0:
				i = 1
				self.hijos['id_' + pregunta_key] = HijoForm()
				for question in preguntas_hijas:
					hijo_key = pregunta_key + '_' + str(i)
					self.hijos['id_' + pregunta_key].crearField(str(question.id),question.getTipo(), question.texto_pregunta, question.preguntas_alternativa.all())
					i = i + 1
			#self.field['hid_'+pregunta_key] = 
			else:
				self.hijos['id_' + pregunta_key] = 0
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

		"""

		for pregunta in PreguntaClasificacion.objects.all():
			respuesta = data[str(pregunta.id)]
			print(respuesta)
			if respuesta == '':
				r = RespuestasClasificacion(pregunta=pregunta, formulario=formulario, puntaje=0, respuesta="")
				r.save()
				continue
			if pregunta.getTipo() == 'a':
				respuesta = TipoAlternativa.objects.get(id=int(respuesta))
				r = RespuestasClasificacion(pregunta=pregunta, formulario=formulario, puntaje=0, respuesta=respuesta)
				r.save()
				continue
			else:
				r = RespuestasClasificacion(pregunta=pregunta, formulario=formulario, puntaje=0, respuesta=respuesta)
				r.save()
				continue

		formulario.respondido = True
		formulario.save()
		print(FormularioClasificacion.objects.filter(empresa=empresa))

			#r = RespuestaClasificacion.objects.get(pregunta=pregunta, formulario=formulario, puntaje=0, respuesta)
		"""
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
            raise  ValidationError("Email ya existe")
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
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user

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
