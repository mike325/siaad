from django.db import models

from apps.Departamentos.models import *

class Asistencia(models.Model):
	id = models.AutoField(primary_key = True)
	fecha = models.DateField(auto_now_add = True)
	horas_clase = models.IntegerField(default = 0)
	asistio = models.BooleanField(default = False)
	fk_contrato = models.ForeignKey(Contrato)

	def __unicode__(self):
		return '%s -> %s: %s'%(self.fecha, self.fk_contrato.fk_curso.fk_profesor, self.asistio)