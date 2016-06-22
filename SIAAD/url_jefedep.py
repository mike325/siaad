# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from apps.Departamentos.urls import *

url_jefedep = [
    url(r'^inicio-jefedep/$', inicio_jefedep, name='inicio_jefedep'),

]

url_jefedep += app_dep_urls
# añade las urls de la app del Departamento