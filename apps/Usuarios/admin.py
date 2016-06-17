from django.contrib import admin
from apps.Usuarios.models import Usuario, Rol
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Rol)