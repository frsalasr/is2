from django.contrib import admin
from .models import * 

admin.site.register(TipoAlternativa)
admin.site.register(TipoElegir)
admin.site.register(Cliente)
admin.site.register(PreguntaDiagnostico)
admin.site.register(RespuestaDiagnostico)
admin.site.register(FormDiagnostico)
admin.site.register(Dimension)
admin.site.register(Etapa)