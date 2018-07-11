from django.db import models
from django.contrib.auth.models import User
import datetime

TIPO_PREGUNTA = (
	('a', 'Alternativa'),
	('n', 'Número'),
	('t', 'Texto'),
	('d', 'Documento')
)

Q_CHOICES = (
	('Idea','Idea'),
	('Semilla','Semilla'),
	('Etapa temprana','Etapa temprana'),
	('Expansion','Expansion'),
	('Internacionalización','Internacionalización'),
)

class Aux(models.Model):
	aux = models.CharField(max_length=255)

	def __str__(self):
		return self.aux

# Alternativa de una pregunta con su texto y su puntaje al ser elegida
class TipoAlternativa(models.Model):
	texto_alternativa = models.CharField(max_length=255)
	puntaje = models.IntegerField(default=0)

	def __str__(self):
		return self.texto_alternativa

# Elección de una pregunta con su texto y su puntaje
class TipoElegir(models.Model):
	texto_eleccion = models.CharField(max_length=255)
	puntaje = models.IntegerField(default=0)

	def __str__(self):
		return self.texto_eleccion

class Cliente(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	telefono = models.IntegerField(null=True, blank=True)
	etapa = models.CharField(max_length=255, choices=Q_CHOICES, default='Idea')

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

class PreguntaClasificacion(models.Model):

	pregunta_base = models.BooleanField(default=False)
	numero = models.IntegerField(unique=False, null=True, blank=True)
	sub_numero = models.IntegerField(unique=False, null=True, blank=True)
	ponderacion = models.IntegerField()
	texto_pregunta = models.CharField(max_length=255)
	tipo_pregunta = models.CharField(max_length=1, choices=TIPO_PREGUNTA, blank=True, default='a')
	preguntas_alternativa = models.ManyToManyField(TipoAlternativa, blank=True)
	preguntas_eleccion = models.ManyToManyField(TipoElegir, blank=True)
	depende_de = models.ManyToManyField("self", blank=True)

	def getTipo(self):
		return self.tipo_pregunta

	def __str__(self):
		return str(self.texto_pregunta)

class FormularioClasificacion(models.Model):
	puntaje = models.FloatField(blank=True, null=True)
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
	preguntas = models.ManyToManyField(PreguntaClasificacion, through='RespuestasClasificacion')

	def __str__(self):
		return str(self.cliente.user.first_name)

class RespuestasClasificacion(models.Model):
	pregunta = models.ForeignKey(PreguntaClasificacion, on_delete=models.CASCADE)
	formulario = models.ForeignKey(FormularioClasificacion, on_delete=models.CASCADE)
	puntaje = models.IntegerField()
	respuesta = models.CharField(max_length=255, blank=True)
	comentario = models.CharField(max_length=255, blank=True, default='')

	def __str__(self):
		return str(str(self.pregunta) + str(self.respuesta))

### MODELOS NUEVOS

"""
class Document(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
	extension = models.CharField(max_length=8, default='none')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def get_upload_path(instance, filename):
		return 'documents/{0}/{1}'.format(instance.empresa.nombre, filename)

	document = models.FileField(upload_to=get_upload_path)

	def getFilename(self):
		import os

		return os.path.basename(str(self.document))

	def __str__(self):
		return str(self.document)
 

"""
class Tiempos(models.Model):
	fecha_guardado = models.DateField(auto_now=True)

class Dimension(models.Model):
	dimension = models.CharField(max_length=255)

class PreguntaDiagnostico(models.Model):
	#id_pregunta = models.IntegerField(primary_key=True)

	Q_CHOICES = (
		(1,1),
		(2,2),
		(3,3),
		(4,4),
		(5,5),
		)

	pregunta_base = models.BooleanField(default=False)
	dimension = models.IntegerField(choices=Q_CHOICES)
	numero = models.IntegerField(unique=False, null=True, blank=True)
	sub_numero = models.IntegerField(unique=False, null=True, blank=True)
	ponderacion = models.IntegerField(default=1)
	texto_pregunta = models.CharField(max_length=255)
	tipo_pregunta = models.CharField(max_length=1, choices=TIPO_PREGUNTA, blank=True, default='a', null=True)
	preguntas_alternativa = models.ManyToManyField(TipoAlternativa, blank=True)
	preguntas_eleccion = models.ManyToManyField(TipoElegir, blank=True)
	depende_de = models.ManyToManyField("self", blank=True)

	class Meta:
		ordering = ['dimension','numero','sub_numero']

	def getTipo(self):
		return self.tipo_pregunta

	def __str__(self):
		return 'Q' + str(self.dimension) + ' ' + str(self.numero) + '.' +str(self.sub_numero) + ' ' + str(self.texto_pregunta)

class FormDiagnostico(models.Model):

	Q_CHOICES = (
		(1,1),
		(2,2),
		(3,3),
		(4,4),
		(5,5),
	)

	ESTADO_CHOICES = (
		('RESUELTO','RESUELTO'),
		('PENDIENTE','PENDIENTE'),
		('CORREGIR','CORREGIR'),
	)

	puntaje = models.FloatField(blank=True, null=True, default=0)
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=True)
	respondido = models.BooleanField(default=False)
	validado = models.BooleanField(default=False)
	editable = models.BooleanField(default=False)
	guardados = models.ManyToManyField(Tiempos)
	estado = models.CharField(max_length=255, default='PENDIENTE', choices=ESTADO_CHOICES)
	fecha_termino = models.DateTimeField(auto_now_add=False, blank=True)
	dimension = models.IntegerField(default=1, choices=Q_CHOICES)
	preguntas = models.ManyToManyField(PreguntaDiagnostico, through='RespuestaDiagnostico')


	"""
	def actualizar(empresa):
		if FormDiagnostico.objects.filter(empresa=empresa).count() == 0:
			return 'error'

		formulario = FormDiagnostico.objects.get(empresa=empresa)
		formulario.Q = empresa.getQbyEtapa()
		formulario.save()

	def construir(empresa):
		if FormDiagnostico.objects.filter(empresa=empresa).count() > 0:
			FormDiagnostico.objects.filter(empresa=empresa).delete()
				
		formulario = FormDiagnostico(empresa=empresa, Q=empresa.getQbyEtapa(), puntaje=0)
		formulario.save()

		for pregunta in PreguntaDiagnostico.objects.all():
			#print(pregunta.texto_pregunta)
			print('creando para ' + pregunta.texto_pregunta)
			r1 = RespuestaDiagnostico(pregunta = pregunta,
										formulario = formulario,
										puntaje=0,
										respuesta='')
			r1.save()

	def responder(self, diccionario):
		# si es que se cambiaron las preguntas
		if self.preguntas.count() != PreguntaDiagnostico.objects.count():
			FormularioClasificacion.construir(self.empresa)

		# se guardan las respuestas correspondientes
		for key,item in diccionario.items():
			#print(str(key) + ' ' + str(item))
			if key == 'csrfmiddlewaretoken':
				continue
			pregunta = PreguntaDiagnostico.objects.get(id=key)
			r1 = RespuestaDiagnostico.objects.get(formulario=self, pregunta=pregunta)
			r1.respuesta = str(item)
			r1.save()

	def addFile(self, documento, id_pregunta):
		print('Inicio models.FormDiagnostico.addFile: ' + str(documento) + ' ' + str(id_pregunta))
		if RespuestaDiagnostico.objects.filter(pregunta=id_pregunta, formulario=self) == 0:
			print('Creando pregunta en blanco . . . ')
			r1 = RespuestaDiagnostico(pregunta = id_pregunta,
							formulario = self,
							puntaje=0,
							respuesta='')
			r1.save()
		r1 = RespuestaDiagnostico.objects.get(pregunta=id_pregunta, formulario=self)
		r1.documento = documento
		r1.save()
		print('Término models.FormDiagnostico.addFIle, creó ' + str(r1.documento))

	def checkFormulario(self):
		if self.preguntas.count() != PreguntaDiagnostico.objects.count():
			preguntas = PreguntaDiagnostico.objects.all()
			for pregunta in preguntas:
				if RespuestaDiagnostico.objects.filter(pregunta=pregunta, formulario=self).count() == 0:
					r1 = RespuestaDiagnostico(pregunta = pregunta,
									formulario = self,
									puntaje=0,
									respuesta='')
					r1.save()

	def calcularPuntaje(self, myDict):
		return 'hola'
	"""

	def __str__(self):
		return self.cliente.user.first_name

class RespuestaDiagnostico(models.Model):
	pregunta = models.ForeignKey(PreguntaDiagnostico, on_delete=models.CASCADE)
	formulario = models.ForeignKey(FormDiagnostico, on_delete=models.CASCADE)
	puntaje = models.IntegerField()
	respuesta = models.CharField(max_length=255, blank=True)
	#documento = models.ForeignKey(Document, on_delete=models.CASCADE, blank=True, null=True)
	buena = models.BooleanField(default=False)

	class Meta:
		ordering = ['formulario','pregunta__dimension','pregunta__numero','pregunta__sub_numero']

	def __str__(self):
		return self.formulario.empresa.nombre + ' Q' + str(self.pregunta.dimension) + ' ' + self.pregunta.texto_pregunta + ' : ' + self.respuesta
