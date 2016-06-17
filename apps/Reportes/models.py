from django.db import models
from apps.Departamentos.models import *

dias_abrev = ['L', 'M', 'I', 'J', 'V', 'S']

class Reporte(models.Model):
	
	id = models.AutoField(primary_key = True)
	fecha = models.DateField(auto_now_add = True)
	fk_contrato = models.ForeignKey(Contrato, default = False)
	fk_depto = models.ForeignKey(Departamento, default = False)
	horasFalta = models.IntegerField()
	comentario = models.CharField(max_length = 100, blank = True)
	
	def __unicode__(self):
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