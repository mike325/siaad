from django.db import models
from django.core.validators import RegexValidator

#import time
from time import strftime

from apps.Usuarios.models import Usuario

numerico = RegexValidator(r'^[0-9]*$', 'Use solo caracteres numericos (0-9).')
alfanumerico = RegexValidator(r'^[0-9a-zA-Z]*$', 'Use solo caracteres alfanumericos (a-Z, 0-9).')

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=20, validators=[alfanumerico], unique=True)
    nombre = models.CharField(max_length=120)
    jefeDep = models.OneToOneField(Usuario, blank=True, null=True)

    def __unicode__(self):
        return self.nombre
        pass

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    fk_departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre
        pass

class Materia(models.Model):
    clave = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=200)
    fk_area = models.ManyToManyField(Area)
    fk_departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.clave
        pass

class Seccion(models.Model):
    id = models.CharField(max_length=5, primary_key=True)

    def __unicode__(self):
        return self.id
        pass    

class Profesor(models.Model):
    codigo_udg = models.CharField(max_length=9, primary_key=True, validators=[numerico])
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s, %s" %(self.apellido, self.nombre)
        pass

class Edificio(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.id
        pass

class Aula(models.Model):
    nombre = models.CharField(max_length=5)
    fk_edif = models.ForeignKey(Edificio)

    def __unicode__(self):
        return self.nombre
        pass

class Ciclo(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    fecha_ini = models.DateField()
    fecha_fin = models.DateField()

    def __unicode__(self):
        return self.id
        pass

class Horario(models.Model):
    id = models.AutoField(primary_key=True)

    hora_ini = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    L = models.BooleanField(default=False, blank=True)
    M = models.BooleanField(default=False, blank=True)
    I = models.BooleanField(default=False, blank=True)
    J = models.BooleanField(default=False, blank=True)
    V = models.BooleanField(default=False, blank=True)
    S = models.BooleanField(default=False, blank=True)

    fk_edif = models.ForeignKey(Edificio, blank=True, null=True)
    fk_aula = models.ForeignKey(Aula, blank=True, null=True)

    def get_dias(self):
        return '-'.join([x for x in 'LMIJVS' if eval('self.'+x)==True])

    def __unicode__(self):
        disp_hora_ini = self.hora_ini.strftime("%H:%M") if self.hora_ini else "no-asignado"
        disp_hora_fin = self.hora_fin.strftime("%H:%M") if self.hora_fin else "no-asignado"
        return "%s-%s : %s"%(
                disp_hora_ini, disp_hora_fin, 
                ''.join([x for x in 'LMIJVS' if eval('self.'+x)==True])
            )
        pass

class Curso(models.Model):
    NRC = models.CharField(max_length=5, primary_key=True) # inmod

    fk_area = models.ForeignKey(Area) # check mod
    
    fk_ciclo = models.ForeignKey(Ciclo) # inmod
    fk_materia = models.ForeignKey(Materia) # inmod
    fk_secc = models.ForeignKey(Seccion)
    
    fk_horarios = models.ManyToManyField(Horario, blank=True)
    
    fk_profesor = models.ForeignKey(Profesor)
    # fk_suplente = models.ForeignKey(Suplente, blank=True, null=True)

    def _str_horarios(self):
        '''
            ejemplo:
            [13:00-14:55, LM]
            [13:00-14:55, LM], [19:00-20:55, I]
        '''
        if self.fk_horarios.all:
            #for index, item in enumerate(items
            ret = ''
            for index, horario in enumerate(self.fk_horarios.all()):
                ret += '[%s-%s'%(
                        horario.hora_ini.strftime("%H:%M"), 
                        horario.hora_fin.strftime("%H:%M")
                    )

                dias = ''.join([
                        x for x in 'LMIJVS' 
                        if eval('horario.'+x)==True
                    ])

                if dias:
                    ret += ' : %s'%dias
                    pass

                ret += ']'
                if index != self.fk_horarios.all().count()-1:
                    ret += ', '
                    pass
                pass

            if not ret:
                return '[(sin horarios)]'
            else:
                return ret
        pass

    def __unicode__(self):
        return self.NRC
        pass

class Suplente(models.Model):
    id = models.AutoField(primary_key=True)
    fk_curso = models.OneToOneField(Curso)
    fk_profesor = models.ForeignKey(Profesor)

    periodo_ini = models.DateField(blank=True, null=True)
    periodo_fin = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id)
        pass

class TipoContrato(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nombre
        pass

class Contrato(models.Model):
    opciones = (
            ('T', 'Tiempo completo'),
            ('P', 'Tiempo parcial'), 
            ('', 'Sin especificar')
        )

    id = models.AutoField(primary_key=True)
    fk_curso = models.ForeignKey(Curso)
    fk_tipocont = models.ForeignKey(TipoContrato, null=True, blank=True)
    
    tipo = models.CharField(max_length=1, choices=opciones, default='', blank=True)

    def __unicode__(self):
        return "%s, %s"%(self.fk_curso, self.tipo)
        pass