from django.contrib import admin
from .models import PreguntaClasificacion, FormularioClasificacion, RespuestasClasificacion, TipoAlternativa, TipoElegir, Cliente
 

admin.site.register(TipoAlternativa)
admin.site.register(TipoElegir)
admin.site.register(PreguntaClasificacion)
admin.site.register(FormularioClasificacion)
admin.site.register(RespuestasClasificacion)
admin.site.register(Cliente)
