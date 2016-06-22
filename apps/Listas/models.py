from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from apps.Departamentos.models import *

@python_2_unicode_compatible
class Asistencia(models.Model):
	id = models.AutoField(primary_key = True)
	fecha = models.DateField(auto_now_add = True)
	horas_clase = models.IntegerField(default = 0)
	asistio = models.BooleanField(default = False)
	fk_contrato = models.ForeignKey(Contrato)

	def __str__(self):
		return '%s -> %s: %s'%(self.fecha, self.fk_contrato.fk_curso.fk_profesor, self.asistio)
