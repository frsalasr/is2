from django.db import models
from django.contrib.auth.models import User

class Ejemplo(models.Model):
	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)


class Postulante(models.Model):
	run = models.CharField(max_length=30, primary_key=True)
	nombre_empresa = models.CharField(max_length=20)
	nombre = models.CharField(max_length=20)
	apellido = models.CharField(max_length=20)
	email = models.EmailField()
	webpage = models.URLField(blank=True, null=True)

	def __str__(self):
		return self.nombre + ' ' + self.apellido

class Formulario(models.Model):
	postulante = models.ForeignKey(Postulante, on_delete=models.CASCADE)
	variable1 = models.IntegerField()
	variable2 = models.IntegerField()
	variable3 = models.IntegerField()
	variable_hid = models.IntegerField(blank=True, null=True)
	result = models.FloatField(blank=True, null=True)

	#setter
	def setResult(self):
		self.result = self.variable1*0.3 + self.variable2*0.2 + self.variable3*0.5

	#getter
	def getResult(self):
		return str(self.result)

	def __str__(self):
		return str(self.result)

def setDependencia():
	for pregunta in PreguntaClasificacion.objects.filter(base_question=True):
		dependientes = PreguntaClasificacion.objects.filter(depende_de=pregunta)
		padre_number = pregunta.numero_pregunta
		i = 1
		for question in dependientes:
			question.numero_pregunta = str(padre_number) + '_' + str(i)
			question.save()
			i = i + 1

##############

TIPO_PREGUNTA = (
	('a', 'Alternativa'),
	('n', 'Número'),
	('t', 'Texto'),
	('d', 'Documento')
	)


class TipoAlternativa(models.Model):
	texto_alternativa = models.CharField(max_length=255)
	puntaje = models.IntegerField()

	def __str__(self):
		return self.texto_alternativa

class TipoElegir(models.Model):
	texto_eleccion = models.CharField(max_length=255)

	def __str__(self):
		return self.texto_eleccion

class PreguntaClasificacion(models.Model):
	#id_pregunta = models.IntegerField(primary_key=True)
	numero_pregunta = models.CharField(unique=True, max_length=255, null=True, blank=True)
	ponderacion = models.IntegerField()
	texto_pregunta = models.CharField(max_length=255)
	tipo_pregunta = models.CharField(max_length=1, choices=TIPO_PREGUNTA, blank=True, default='a', null=True)
	preguntas_alternativa = models.ManyToManyField(TipoAlternativa, blank=True)
	#preguntas_eleccion = models.ManyToManyField(TipoElegir, blank=True)
	base_question = models.BooleanField(default=False)
	#hijo_de = models.IntegerField(default=0)
	depende_de = models.ManyToManyField("self", blank=True)

	def getTipo(self):
		return self.tipo_pregunta

	def __str__(self):
		return str(self.texto_pregunta)


class Empresa(models.Model):
	rut = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=255)
	etapa = models.CharField(max_length=255,blank=True, null=True)
	autor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def getQbyEtapa(self):
		if self.etapa == 'idea':
			return 1
		elif self.etapa == 'semilla':
			return 2
		elif self.etapa == 'xxx':
			return 3
		elif self.etapa == 'asd':
			return 4
		else:
			return 5

	def setEtapa(self, etapa):
		self.etapa = etapa
		self.save()
		print('etapa ' + self.etapa)
	
	def __str__(self):
		return str(self.nombre)

class FormularioClasificacion(models.Model):
	#id_formulario = models.IntegerField(primary_key=True)
	puntaje = models.FloatField(blank=True, null=True)
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
	preguntas = models.ManyToManyField(PreguntaClasificacion, through='RespuestasClasificacion')
	respondido = models.BooleanField(default=False)
	validado = models.BooleanField(default=False)
	comentario = models.CharField(max_length=512, blank=True, default='')

	def construir(empresa):
		if FormularioClasificacion.objects.filter(empresa=empresa).count() > 0:
			FormularioClasificacion.objects.filter(empresa=empresa).delete()
				
		formulario = FormularioClasificacion(empresa=empresa, puntaje=0)
		formulario.save()

		for pregunta in PreguntaClasificacion.objects.all():
			#print(pregunta.texto_pregunta)
			print('creando para ' + pregunta.texto_pregunta)
			r1 = RespuestasClasificacion(pregunta = pregunta,
										formulario = formulario,
										puntaje=0,
										respuesta='')
			r1.save()
			#r2 = RespuestasClasificacion.objects.get(pregunta=pregunta, formulario=formulario)
			#print(r2)

	def ponerPuntaje(myDict, empresa):
	
		if FormularioClasificacion.objects.filter(empresa=empresa).count() > 0:
			FormularioClasificacion.objects.filter(empresa=empresa).delete()

		formulario = FormularioClasificacion(empresa=empresa, puntaje=0)
		formulario.save()

		for pregunta in PreguntaClasificacion.objects.all():
			r1 = RespuestasClasificacion(pregunta=pregunta,
										 formulario=formulario,
										 puntaje=0,
										 respuesta='')
			r1.save()
			print('r1 ' + r1.pregunta.texto_pregunta)

			if myDict.get(str(pregunta.id)):
				#print(pregunta.texto_pregunta)
				#print(TipoAlternativa.objects.get(id=myDict.get(str(pregunta.id))).puntaje)
				r2 = RespuestasClasificacion.objects.get(pregunta=pregunta, formulario=formulario)
				print('r2 ' + r2.pregunta.texto_pregunta)
				r2.puntaje = TipoAlternativa.objects.get(id=myDict.get(str(pregunta.id))).puntaje
				#print(TipoAlternativa.objects.get(id=myDict.get(str(pregunta.id))).texto_alternativa)
				r2.respuesta = 	TipoAlternativa.objects.get(id=myDict.get(str(pregunta.id))).texto_alternativa
				r2.save()
		#print('respuestas de este form:')
		#FormularioClasificacion.construir(empresa)		
		
		puntaje = 0
		for question in RespuestasClasificacion.objects.filter(formulario=formulario):
			puntaje = puntaje + question.pregunta.ponderacion*question.puntaje

		puntaje = puntaje/PreguntaClasificacion.objects.all().count()
		print('puntaje ' + str(puntaje))


		formulario.puntaje = puntaje
		formulario.save()

		if puntaje < 5:
			formulario.empresa.setEtapa('idea')
		elif puntaje >= 5 and puntaje < 10:
			formulario.empresa.setEtapa('semilla')
		else:
			formulario.empresa.setEtapa('pyme')

		formulario.respondido = True
		formulario.save()

		#print(RespuestasClasificacion.objects.filter(formulario=formulario))

	def calcularPuntaje(formulario):
		preguntas = RespuestasClasificacion.objects.filter(formulario=formulario)
		puntaje = 0
		for question in preguntas:
			puntaje = puntaje + question.pregunta.ponderacion*question.puntaje
		print(puntaje)
		formulario.puntaje = puntaje/PreguntaClasificacion.objects.all().count()
		formulario.save()

	def setEtapa(formulario):
		if formulario.puntaje < 4:
			formulario.empresa.setEtapa('idea')
		elif formulario.puntaje >= 3 and formulario.puntaje < 10:
			formulario.empresa.setEtapa('semilla')
		else:
			formulario.empresa.setEtapa('pyme')

	def __str__(self):
		return str(self.empresa.nombre)

class RespuestasClasificacion(models.Model):
	pregunta = models.ForeignKey(PreguntaClasificacion, on_delete=models.CASCADE)
	formulario = models.ForeignKey(FormularioClasificacion, on_delete=models.CASCADE)
	puntaje = models.IntegerField()
	respuesta = models.CharField(max_length=255, blank=True)
	comentario = models.CharField(max_length=255, blank=True, default='')

	def __str__(self):
		return str(str(self.pregunta) + str(self.respuesta))

### MODELOS NUEVOS


class Document(models.Model):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
	extension = models.CharField(max_length=8, default='none')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def get_upload_path(instance, filename):
		return 'documents/{0}/{1}'.format(instance.empresa.nombre, filename)

	document = models.FileField(upload_to=get_upload_path)

	def __str__(self):
		return str(self.document)
 
class PreguntaDiagnostico(models.Model):
	#id_pregunta = models.IntegerField(primary_key=True)

	Q_CHOICES = (
		(1,1),
		(2,2),
		(3,3),
		(4,4),
		(5,5),
		)

	base_question = models.BooleanField(default=False)
	Q = models.IntegerField(choices=Q_CHOICES)
	numero = models.IntegerField(unique=False, null=True, blank=True)
	sub_numero = models.IntegerField(unique=False, null=True, blank=True)
	ponderacion = models.IntegerField(default=1)
	texto_pregunta = models.CharField(max_length=255)
	tipo_pregunta = models.CharField(max_length=1, choices=TIPO_PREGUNTA, blank=True, default='a', null=True)
	preguntas_alternativa = models.ManyToManyField(TipoAlternativa, blank=True)
	
	depende_de = models.ManyToManyField("self", blank=True)
	document = models.BooleanField(default=False)

	class Meta:
		ordering = ['Q','numero','sub_numero']

	def getTipo(self):
		return self.tipo_pregunta

	def __str__(self):
		return 'Q' + str(self.Q) + ' ' + str(self.numero) + '.' +str(self.sub_numero) + ' ' + str(self.texto_pregunta)

class FormDiagnostico(models.Model):

	Q_CHOICES = (
		(1,1),
		(2,2),
		(3,3),
		(4,4),
		(5,5),
		)

	puntaje = models.FloatField(blank=True, null=True, default=0)
	empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, unique=True)
	respondido = models.BooleanField(default=False)
	validado = models.BooleanField(default=False)
	editable = models.BooleanField(default=False)
	comentario = models.CharField(max_length=512, blank=True, default='')
	Q = models.IntegerField(default=1, choices=Q_CHOICES)
	preguntas = models.ManyToManyField(PreguntaDiagnostico, through='RespuestaDiagnostico')

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



	def __str__(self):
		return self.empresa.nombre

class RespuestaDiagnostico(models.Model):
	pregunta = models.ForeignKey(PreguntaDiagnostico, on_delete=models.CASCADE)
	formulario = models.ForeignKey(FormDiagnostico, on_delete=models.CASCADE)
	puntaje = models.IntegerField()
	respuesta = models.CharField(max_length=255, blank=True)
	comentario = models.CharField(max_length=255, blank=True, default='')
	documento = models.ForeignKey(Document, on_delete=models.CASCADE, blank=True, null=True)
	buena = models.BooleanField(default=False)

	class Meta:
		ordering = ['formulario','pregunta__Q','pregunta__numero','pregunta__sub_numero']

	def __str__(self):
		return self.formulario.empresa.nombre + ' Q' + str(self.pregunta.Q) + ' ' + self.pregunta.texto_pregunta + ' : ' + self.respuesta