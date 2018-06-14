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

	def ordenar(formulario):
		ordenado = []
		bases = PreguntaClasificacion.objects.filter(base_question=True).order_by('-numero_pregunta')

		for question in bases:
			ans = RespuestasClasificacion.objects.get(pregunta=question, formulario=formulario)
			aux = [question.texto_pregunta,ans.respuesta]
			hijos = PreguntaClasificacion.objects.filter(depende_de=question)
			aux2 = []
			for hijo in hijos:
				ans = RespuestasClasificacion.objects.get(pregunta=hijo, formulario=formulario)
				aux2.append([hijo.texto_pregunta, ans.respuesta])

			ordenado.append([aux,aux2])

		return ordenado


		return dict_ordenado


	def __str__(self):
		return str(str(self.pregunta) + str(self.respuesta))