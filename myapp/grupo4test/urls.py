from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    #path('', views.base, name='base'),
    ## PAGINA DE INICIO
    path('', views.home, name='home'),

	# registro de usuarios
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/',views.register, name='register'),

    ### CLIENTE

    # formularios
    path('formulario/',views.formulario, name='formulario'),
    path('datos/',views.datos, name='datos'),
    path('diagnostico/',views.diagnostico,name='diagnostico'),

    # ejemplo
    path('ejemplo/', views.ejemplo, name='ejemplo'),
    ### ADMINS
    # ver postulantes
    path('postulantes/clasificacion', views.clasificados, name='clasificados'),
    path('postulantes/diagnostico', views.diagnosticados, name='diagnosticados'),

    # empresa en particular 
    path('postulantes/clasificacion/<int:rut_empresa>', views.clasificar, name='clasificar'),

    #guardar archivo
    path('wea/', views.wea, name='wea'),
]