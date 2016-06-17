from django.conf.urls import include, url
from django.contrib import admin

from apps.Reportes.views import *
from apps.Listas.views import *

url_secretaria = [
	url(r'^inicio-secretaria/$', inicio_secretaria, name='inicio_secretaria'),
	url(r'^(?P<dpto>.+)/listas/tCompleto$', listas_tCompleto),
	url(r'^(?P<dpto>.+)/listas/tMedio$', listas_tMedio),
	url(r'^(?P<dpto>.+)/form-incidencias$', form_incidencias),
	url(r'^(?P<dpto>.+)/form-reporte-incidencias$', form_reporte_incidencias),
	url(r'^(?P<dpto>.+)/ver-incidencias$', ver_incidencias),
	url(r'^(?P<dpto>.+)/reporte-incidencias$', reporte_incidencias),
    url(r'^estadisticas-profesor/$', estadisticasProfesor, name='estadisticas_profesor'),
    url(r'^estadisticas-materia/$', estadisticasMateria, name='estadisticas_materia'),
    url(r'^estadisticas-ciclo/$', estadisticasCiclo, name='estadisticas_ciclo'),
    url(r'^(?P<dpto>.+)/estadisticas-departamento/$', estadisticasDepartamento, name='estadisticas_departamento'),
]