# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Rol(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=15)

    def __str__(self):
        return self.tipo
        pass

@python_2_unicode_compatible
class Usuario(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    codigo = models.CharField(max_length=9, unique=True)
    rol = models.ForeignKey(Rol)

    def __str__(self):
        return self.user.username
        pass

    @classmethod
    def alta_jefe(cls, username, password, first_name, last_name, email, codigo):
        nuevo_user = User.objects.create_user(username=username, password=password,
                                     first_name=first_name, last_name=last_name, email=email)
        nuevo_user.save()
        usuario = cls(user=nuevo_user, codigo=codigo, rol=Rol.objects.get(id=2))
        return usuario

    @classmethod
    def alta_secretaria(cls, username, password, first_name, last_name, email, codigo):
        nuevo_user = User.objects.create_user(username=username, password=password,
                                     first_name=first_name, last_name=last_name, email=email)
        nuevo_user.save()
        usuario = cls(user=nuevo_user, codigo=codigo, rol=Rol.objects.get(id=1))
        return usuario

    @classmethod
    def hacer_jefe(self):
        self.rol = Rol.objects.get(id=2)
        return self

    @classmethod
    def hacer_secretaria(self):
        self.rol = Rol.objects.get(id=1)
        return self
