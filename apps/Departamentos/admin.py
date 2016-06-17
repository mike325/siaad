from django.contrib import admin
from .models import *

# Es necesario registrar en admin para el proyecto?
admin.site.register(Departamento)
admin.site.register(Area)
admin.site.register(Materia)
admin.site.register(Seccion)
admin.site.register(Profesor)
admin.site.register(Edificio)
admin.site.register(Aula)
admin.site.register(Ciclo)
admin.site.register(Horario)
admin.site.register(Curso)
admin.site.register(Suplente)
admin.site.register(Contrato)
admin.site.register(TipoContrato)