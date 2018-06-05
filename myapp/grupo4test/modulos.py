from .models import *
from django.db import transaction

# checkea si el run existe
def checkPostulante(run):
	if Postulante.objects.filter(run=run).count() > 0:
		return True
	return False

# añade un usuario 
def addUser(run, nombre_empresa,nombre,apellido,email,url):
	postulante = Postulante(run=run,
							nombre_empresa=nombre_empresa,
							nombre=nombre,
							apellido=apellido,
							email=email,
							webpage=url)
	postulante.save()

# checkea si el run corresponde a la empresa
def checkRunEmpresa(run, nombre_empresa):
	print(Postulante.objects.get(run=run).nombre_empresa)
	print(nombre_empresa)
	if Postulante.objects.get(run=run).nombre_empresa == nombre_empresa:
		return True
	return False

# retorna empresa por run
def getEmpresaByRun(run):
	return Postulante.objects.get(run=run).nombre_empresa

##########
