from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from .views import Pdf

from . import views

urlpatterns = [
    #path('', views.base, name='base'),
    ## PAGINA DE INICIO
    #path('', views.home, name='home'),
    path('', views.home, name='home'),

    path('login/', views.login, name='view_login'),
	# registro de usuarios
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/',views.register, name='register'),
    path('register2/',views.register2, name='register2'),
    path('register3/',views.register3, name='register3'),

    ### CLIENTE

    # formularios
    path('formulario/',views.formulario, name='formulario'),
    path('datos/',views.datos, name='datos'),
    path('diagnostico/',views.diagnostico,name='diagnostico'),

    # ejemplo
    path('ejemplo/', views.ejemplo, name='ejemplo'),

    ### ADMINS
    # ver postulantes
    path('postulantes/clasificacion/', views.clasificados, name='clasificados'),
    path('postulantes/diagnostico/', views.diagnosticados, name='diagnosticados'),
    path('postulantes/id/<int:id_cliente>', views.cliente, name='cliente'),
    
    # empresa en particular 
    path('postulantes/clasificacion/<int:rut_empresa>', views.clasificar, name='clasificar'),
    path('postulantes/diagnostico/<int:rut_empresa>', views.diagnosticar, name='diagnosticar'),

    #guardar archivo
    path('save/', views.save, name='save'),

    #pdf
    path('pdf/<int:id_cliente>', Pdf.as_view(), name='pdf'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()