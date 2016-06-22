from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from apps.Departamentos.models import *

dias_abrev = ['L', 'M', 'I', 'J', 'V', 'S']

@python_2_unicode_compatible
class Reporte(models.Model):
	
	id = models.AutoField(primary_key = True)
	fecha = models.DateField(auto_now_add = True)
	fk_contrato = models.ForeignKey(Contrato, default = False)
	fk_depto = models.ForeignKey(Departamento, default = False)
	horasFalta = models.IntegerField()
	comentario = models.CharField(max_length = 100, blank = True)
	
	def __str__(self):
		return '%s -> %s'%(self.fecha, self.fk_contrato.fk_curso.fk_profesor)
		pass

	def getHorario(self):
		filtro = {dias_abrev[self.fecha.weekday()]: True}
		horarios = self.fk_contrato.fk_curso.fk_horarios.filter(**filtro)

		dias = []
		ret = { 'horarios': horarios }

		for horario in horarios:
			dias.append( horario.get_dias() )
			pass

		ret.update({ 'dias': dias })

		return ret
