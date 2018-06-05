from django.contrib import admin
from .models import PreguntaClasificacion, Empresa, FormularioClasificacion, RespuestasClasificacion, TipoAlternativa, TipoElegir

admin.site.register(TipoAlternativa)
admin.site.register(TipoElegir)
admin.site.register(PreguntaClasificacion)
admin.site.register(FormularioClasificacion)
admin.site.register(RespuestasClasificacion)
admin.site.register(Empresa)


