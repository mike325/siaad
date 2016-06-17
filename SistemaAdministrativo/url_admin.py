from django.conf.urls import include, url
from django.contrib import admin

from apps.Usuarios.views import *
from apps.Historicos.views import *

url_admin = [
    url(r'^$', login, name='login'),
    url(r'^login/$', login),
    url(r'^logout/$', logout, name='logout'),
	url(r'^inicio-administrador/$', inicio_admin, name='inicio_admin'),
    url(r'^(?P<dpto>.+)/modificar/jefe-departamento', sistema_modificar_jefedep),
    url(r'^nuevo_departamento',nuevo_departamento),
    url(r'^activar_usuarios',activar_usuarios),
    url(r'^nuevo_jefe',nuevo_jefe),
    url(r'^nueva_secretaria/$', nueva_secretaria),
    url(r'^(?P<dpto>.+)/historicos/$', historicos),
    url(r'^(?P<dpto>.+)/historicos/filtro/$', historicosFiltrados),
    url(r'^modificar-perfil/$',modificar_perfil),
    url(r'^modificar-password/$',modificar_password), 
    
]