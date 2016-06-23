# -*- encoding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import date, time, datetime, timedelta
from collections import Counter
from django.db.models import Q

from apps.Departamentos.models import *
from apps.Reportes.models import *
from apps.Historicos.models import *
from apps.Listas.models import *

import re, math

from siaad.commons.shortcuts import get_ciclo_vigente

'''
FIX:
	+ Agregadas constantes de template.

	+ Formulario para Estadisticas de Profesor ahora muestra los profesores
	  en orden alfabetico por apellido.

	+ 'cicloActual' se estaba basando en el ciclo cuya fecha de inicio 
	  fuera la más antigua.
		^ Adicionalmente, se actualizó la condicion en todos filtros 
		  para coincidir con el valor que retorna 'get_ciclo_vigente'
'''

# Override del día
DAY_OVR = 2

dias_abrev = ['L', 'M', 'I', 'J', 'V', 'S']
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

TEMPLATE_ESTADISTICAS_LISTAS = 'Listas/estadisticas-listas.html'
TEMPLATE_LISTAS = 'Listas/listas.html'

#Creacion de la lista de asistencias para profesores de tiempo completo
def crear_lista_diaria_TCompleto(request, dpto):
	hoy = date.today()
	dia = hoy.isoweekday()
	dpto = Departamento.objects.get(nick=dpto)

	'''
	Override del día para pruebas.
	(COMENTAR O ELIMINAR PARA PRODUCCION)
	'''
	# dia = DAY_OVR # DEBUG

	_profesor = None
	filtro = {}

	for clave, valor in request.POST.items():
		if not clave.startswith('csrf'): # no tiene que ver con el key CSRF
			_profesor = Profesor.objects.get(
					codigo_udg=str(clave)
				) ## GG OPT

			filtro = { 'fk_curso__fk_horarios__' + dias_abrev[dia-1]: True }
			contratos = Contrato.objects.filter(
					tipo='T',
					fk_curso__fk_profesor=_profesor,
					**filtro
				) ## GG OPT

			filtro = { dias_abrev[dia-1]: True }

			_asistencia = None
			tipoActual = contratos[0].fk_tipocont
			for contrato in contratos:
				assist = Asistencia()
				assist.asistio = True if valor=='on' else False
				assist.fk_contrato = contrato

				# PREPARACIONES HORAS DE CLASE >> inicio
				horas_clase = None
				for x in contrato.fk_curso.fk_horarios.filter(**filtro):
					hora_ini = datetime.combine(hoy, x.hora_ini)
					hora_fin = datetime.combine(hoy, x.hora_fin)

					if horas_clase:
						horas_clase = horas_clase + (hora_fin - hora_ini)
					else:
						horas_clase = hora_fin - hora_ini

					#print horas_clase # DEBUG
					pass # for
				# PREPARACIONES HORAS DE CLASE >> fin

				horas = horas_clase.seconds/60
				assist.horas_clase = int(math.ceil(horas/60.0))
				assist.save()

				# print assist # DEBUG
				pass # for 
			pass # if
		pass # for
	historico = Registro.creacion(request.session['usuario']['nick'],
		  'Se guardaron las asistencias de Tiempo Completo del "'+ dpto.nombre +'"',
		  'Guardadas', 'Asistencias', dpto)
	historico.save()

	return redirect("/")
	pass # view

def crear_lista_diaria_TMedio(request, dpto):
	hoy = date.today()
	dia = hoy.isoweekday()
	dpto = Departamento.objects.get(nick=dpto)

	'''
	Override del día para pruebas.
	(COMENTAR O ELIMINAR PARA PRODUCCION)
	'''
	# dia = DAY_OVR # DEBUG

	'''
		REV: Horario puede que no se ocupe aqui
	'''

	filtro = { dias_abrev[dia-1]: True }

	for clave, valor in request.POST.items():
		#print clave, '\t\t', valor
		if not clave.startswith('csrf'): # no tiene que ver con el key CSRF
			_contrato = Contrato.objects.get(id=clave)
			assist = Asistencia()
			assist.fk_contrato = _contrato
			assist.asistio = True if valor=='on' else False

			# PREPARACIONES HORAS DE CLASE >> inicio
			horas_clase = None
			for x in _contrato.fk_curso.fk_horarios.filter(**filtro):
				hora_ini = datetime.combine(hoy, x.hora_ini)
				hora_fin = datetime.combine(hoy, x.hora_fin)

				if horas_clase:
					horas_clase = horas_clase + (hora_fin - hora_ini)
				else:
					horas_clase = hora_fin - hora_ini

				#print horas_clase # DEBUG
				pass # for
			# PREPARACIONES HORAS DE CLASE >> fin

			horas = horas_clase.seconds/60
			assist.horas_clase = int(math.ceil(horas/60.0))

			assist.save() # GUARDA LOS DATOS
			#print assist

			pass # if
		pass # for

	historico = Registro.creacion(request.session['usuario']['nick'],
					'Se guardaron las asistencias de Medio Tiempo del "'+ dpto.nombre +'"',
					'Guardadas', 'Asistencias', dpto)
	historico.save()

	return redirect('/')

#Listas de tiempo completo
@login_required(login_url='/')
def listas_tCompleto(request, dpto):
	if request.session['rol'] >= 1:
		if request.method == 'POST':
			return crear_lista_diaria_TCompleto(request, dpto)
		else:
			dpto = get_object_or_404(Departamento, nick = dpto)
			hoy = date.today()
			dia = hoy.isoweekday()
			
			disp_dia = dias[dia - 1].upper()
			disp_num_dia = str(hoy.day)
			disp_mes = meses[hoy.month - 1].upper()
			disp_anio = str(hoy.year)

			fechaDia = disp_dia + " " + disp_num_dia + " DE " + disp_mes + " DE " + disp_anio

			'''
			Override del día para pruebas.
			(COMENTAR O ELIMINAR PARA PRODUCCION)
			'''
			# dia = DAY_OVR # DEBUG

			if dia >= 7: 
			# si es domingo o por alguna extraña 
			# razon salió un día mas alto
				raise Http404 # pues nada

			profesores = Profesor.objects.filter(
					curso__fk_area__fk_departamento=dpto,
					curso__fk_ciclo__in=get_ciclo_vigente()
				).distinct().order_by('apellido').select_related()

			filtro = {'fk_horarios__'+dias_abrev[dia-1]: True}

			#cursos = Curso.objects.filter(**filtro)

			listaAsistencia = []

			for x in profesores:
				cursos = x.curso_set.filter(
						fk_profesor=x,
						contrato__isnull=False, # todos los cursos con un contrato
						fk_area__fk_departamento=dpto, # que tengan el departamento
						**filtro # más el filtro extra
					)
				contratos = Contrato.objects.filter(
						tipo='T',
						fk_curso__in=cursos
					).values('fk_tipocont__nombre')
				horarios = Horario.objects.filter(
						curso__in=cursos
					).order_by('hora_ini')#.values()

				cuenta = horarios.count()

				suplencias = Suplente.objects.filter(
						Q(fk_curso__in=cursos),
						Q(periodo_ini__lte=hoy) | Q(periodo_ini__isnull=True),
						Q(periodo_fin__gte=hoy) | Q(periodo_fin__isnull=True)
					)

				if contratos and cuenta > 0:
					listaAsistencia.append({
							'profesor': x.apellido + ', ' + x.nombre + '(' + x.codigo_udg + ')',
							'suplente': suplencias,
							'hora_ini': horarios[0].hora_ini,
							'hora_fin': horarios[cuenta-1].hora_fin,
							'codigo_prof': x.codigo_udg
						})
					pass
				pass

				'''DESCOMENTAR SI QUIERE ORDENARSE POR HORA DE INICIO'''
				#listaAsistencia = sorted(listaAsistencia, key=lambda d: (d['hora_ini'], d['profesor']))

			yaRegistradas = Asistencia.objects.filter(
					fecha__startswith = hoy,
					fk_contrato__tipo = 'T',
					fk_contrato__fk_curso__fk_materia__fk_departamento__nick = dpto.nick
				).count()
			yaRegistradas = yaRegistradas!=0
			# print yaRegistradas # DEBUG
			return render(request, TEMPLATE_LISTAS,
				{
					'today': fechaDia, 
					'tiempoC': True,
					'listaAsistencia' : listaAsistencia,
					'horarios' : horarios,
					'yaRegistradas' : yaRegistradas
				})
	else:
		return redirect('error403', origen=request.path)

#Listas de medio tiempo
@login_required(login_url='/')
def listas_tMedio(request, dpto):
	if request.session['rol'] >= 1:
		if request.method == 'POST':
			return crear_lista_diaria_TMedio(request, dpto)
		else:
			dpto = get_object_or_404(Departamento, nick=dpto)
			hoy = date.today()
			dia = hoy.isoweekday()
			mes_num = int(hoy.month)

			disp_dia = dias[dia-1].upper()
			disp_mes = meses[mes_num-1][:3].upper()

			'''
			Override del día para pruebas.
			(COMENTAR O ELIMINAR PARA PRODUCCION)
			'''
			# dia = DAY_OVR # DEBUG

			if dia >= 7: 
			# si es domingo o por alguna extraña 
			# razon salió un día mas alto
				raise Http404 # pues nada

			filtro = { dias_abrev[dia-1]: True }

			horarios = Horario.objects.filter(**filtro)

			yaRegistradas = Asistencia.objects.filter(
					fecha__startswith = hoy,
					fk_contrato__tipo = 'P',
					fk_contrato__fk_curso__fk_materia__fk_departamento = dpto
				).count()
			yaRegistradas = yaRegistradas!=0

			cursosTMedio = Contrato.objects.filter(
					tipo = 'P',
					fk_curso__fk_ciclo=get_ciclo_vigente(),
					fk_curso__fk_horarios__in = horarios,
					fk_curso__fk_area__fk_departamento = dpto
				).order_by(
					'fk_curso__fk_horarios__hora_ini',
					'fk_curso__fk_profesor__apellido'
				).select_related()

			suplentes = Suplente.objects.filter(
					Q(periodo_ini__lte=hoy) | Q(periodo_ini__isnull=True),
					Q(periodo_fin__gte=hoy) | Q(periodo_fin__isnull=True)
				)

			return render(request, TEMPLATE_LISTAS, 
				{
					'tiempoM': True,
					'departamento': dpto,
					'dayWeek': disp_dia, 
					'day': hoy.day, 
					'month': disp_mes, 
					'year': hoy.year, 

					'horarios' : horarios,
					'listaContratos' : cursosTMedio,
					'yaRegistradas' : yaRegistradas,
					'lista_suplentes': suplentes
				})
	else:
		return redirect('error403', origen=request.path)


''' Apartado de estaticas sobre asistencias '''

#Estadisticas de asistencia de un depto.
@login_required(login_url='/')
def estadisticasDepartamento(request, dpto):
	if request.session['rol'] >= 1:
		departamento = get_object_or_404(Departamento, nick=dpto)
		try:
			datos = {}
			tablaMaterias = {}

			#Aquí se genera la información que se pasará a la gráfica
			cicloActual = get_ciclo_vigente()

			# Si la peticion incluye fecha de inicio y fecha fin
			if request.GET.get('fechaI','') and request.GET.get('fechaF',''):
				fechaI = request.GET.get('fechaI')
				fechaF = request.GET.get('fechaF')
				asistenciasTotales = Asistencia.objects.filter(
							fk_contrato__fk_curso__fk_ciclo__in=cicloActual,
							fk_contrato__fk_curso__fk_materia__fk_departamento=departamento,
							fecha__range=[fechaI , fechaF]
							)
				datos.update({
					'fechaI':fechaI,
					'fechaF':fechaF,
					})
			else: # Obtiene los datos normalmente
				asistenciasTotales = Asistencia.objects.filter(
							fk_contrato__fk_curso__fk_ciclo__in=cicloActual,
							fk_contrato__fk_curso__fk_materia__fk_departamento=departamento
							)

			materiasTC = asistenciasTotales.filter(fk_contrato__tipo='T')
			materiasTM = asistenciasTotales.filter(fk_contrato__tipo='P')

			#Lista de valores para filtrar repetidos
			valores = materiasTC.values_list('fk_contrato__fk_curso__NRC',
											'fk_contrato__fk_tipocont__id').distinct()
			materias = asistenciasTotales.values_list('fk_contrato__fk_curso__fk_materia__clave',
													'fk_contrato__fk_curso__fk_materia__nombre').distinct()

			#Filtrando valores repetidos
			for x in valores:
				materiasTM = materiasTM.exclude(fk_contrato__fk_curso__NRC=x[0],
												fk_contrato__fk_tipocont__id=str(x[1]))

			asistenciasTotales = materiasTC | materiasTM

			for x in materias:
				key = x[0]
				if key not in tablaMaterias:
					materiaAsistencias =  asistenciasTotales.filter(asistio=True,
									fk_contrato__fk_curso__fk_materia__clave=key).count()
					materiaInasistencias =  asistenciasTotales.filter(asistio=False,
									fk_contrato__fk_curso__fk_materia__clave=key).count()

					total = materiaAsistencias+materiaInasistencias

					if total == 0.0 : continue #Evitar que de error al intentar dividir entre 0
					asistenciasP = round(100 * float(materiaAsistencias)/float(total), 2)
					inasistenciasP = round(100 * float(materiaInasistencias)/float(total), 2)

					tablaMaterias.update(
						{key:{
							'nombre': x[1],
							'clave' : key,
							'asistencias' : '%s(%s%%)'%(materiaAsistencias, asistenciasP),
							'inasistencias' :'%s(%s%%)'%(materiaInasistencias,inasistenciasP),
							'total' : total
						}})

			#Datos que se cargaran a la gráfica
			datos.update({
				'dpto' : departamento,
				'nombre' : departamento.nombre,
				'asistenciasTotales' : asistenciasTotales.count(),
				'asisTCompleto' : materiasTC.filter(asistio=True).count(),
				'asisTMedio' : materiasTM.filter(asistio=True).count(),
				'inasisTCompleto' : materiasTC.filter(asistio=False).count(),
				'inasisTMedio' : materiasTM.filter(asistio=False).count()
			})
			return render(request, 'Listas/estadisticas-departamento.html', locals())
			pass
		except:
			return redirect('/inicio-secretaria/')
	else:
		return redirect('error403', origen=request.path)

#Estadisticas de asistencia de un profesor
@login_required(login_url='/')
def estadisticasProfesor(request):
	if request.session['rol'] >= 1:
		if request.GET.get('profesor'):
			profesor = get_object_or_404(Profesor, codigo_udg=request.GET.get('profesor'))
			try:
				#Aquí se genera la información que se pasará a la gráfica

				datos = {}
				tablaTCompleto = {}
				tablaTMedio = {}

				cicloActual = get_ciclo_vigente()

				if request.POST.get('fechaI','') and request.POST.get('fechaF',''):
					fechaI = request.POST.get('fechaI')
					fechaF = request.POST.get('fechaF')
					asistenciasTotales = Asistencia.objects.filter(
									fk_contrato__fk_curso__fk_ciclo__in=cicloActual,
									fk_contrato__fk_curso__fk_profesor=profesor,
									fecha__range=[fechaI , fechaF]
									)
					datos.update({
						'fechaI':fechaI,
						'fechaF':fechaF,
					})
				else:
					asistenciasTotales = Asistencia.objects.filter(
									fk_contrato__fk_curso__fk_ciclo__in=cicloActual,
									fk_contrato__fk_curso__fk_profesor=profesor
									)

				faltasTotales = asistenciasTotales.filter(asistio=False)

				asistenciasTotalesTC = asistenciasTotales.filter(fk_contrato__tipo='T')
				asistenciasTC = asistenciasTotalesTC.filter(asistio=True)
				faltasTC = asistenciasTotalesTC.filter(asistio=False)
				valores = asistenciasTotalesTC.values_list('fk_contrato__fk_curso__NRC',
																 'fk_contrato__fk_tipocont__id').distinct()
				contratos = Contrato.objects.filter(
								fk_curso__fk_profesor=profesor).values_list('id', flat=True).distinct()

				# print contratos

				asistenciasTotalesTM = asistenciasTotales.filter(fk_contrato__tipo='P')

				for x in valores:
					asistenciasTotalesTM = asistenciasTotalesTM.exclude(
												fk_contrato__fk_curso__NRC=x[0],
												fk_contrato__fk_tipocont__id=str(x[1]))

				asistenciasTM = asistenciasTotalesTM.filter(asistio=True)
				faltasTM = asistenciasTotalesTM.filter(asistio=False)

				#Informacion detallada que se muestra en la tabla
				#Tabla de tiempo completo
				for key in contratos:
					if key not in tablaTCompleto:
						contrato = Contrato.objects.get(id=key)
						asistencias = asistenciasTC.filter(fk_contrato__id=key).count()
						inasistencias = faltasTC.filter(fk_contrato__id=key).count()
						total = asistencias+inasistencias
						if total == 0.0 : continue #Evitar que de error al intentar dividir entre 0
						asistP = round(100 * float(asistencias)/float(total), 2)
						inasistP = round(100 * float(inasistencias)/float(total), 2)

						tablaTCompleto.update(
							{key:
								{'tipoContrato' : contrato.fk_tipocont,
								'nombre': contrato.fk_curso.fk_materia.nombre,
								'secc' : contrato.fk_curso.fk_secc,
								'asist' : "%s (%s%%)"%(asistencias, asistP),
								'inasist' : "%s (%s%%)"%(inasistencias, inasistP),
								'total' : total
								}})
				
				#Tabla de medio tiempo
				for key in contratos:
					if key not in tablaTMedio:
						contrato = Contrato.objects.get(id=key)
						asistencias = asistenciasTM.filter(fk_contrato__id=key).count()
						inasistencias = faltasTM.filter(fk_contrato__id=key).count()
						total = asistencias+inasistencias
						if total == 0.0 : continue #Evitar que de error al intentar dividir entre 0
						asistP = round(100 * float(asistencias)/float(total), 2)
						inasistP = round(100 * float(inasistencias)/float(total), 2)

						tablaTMedio.update(
							{key:
								{'tipoContrato' : contrato.fk_tipocont,
								'nombre': contrato.fk_curso.fk_materia.nombre,
								'secc' : contrato.fk_curso.fk_secc,
								'asist' : "%s (%s%%)"%(asistencias, asistP),
								'inasist' : "%s (%s%%)"%(inasistencias, inasistP),
								'total' : total
								}})

				#Datos que se cargaran a la gráfica
				datos.update({
					'nombre' : (profesor.nombre + " " + profesor.apellido +
								 "(" + profesor.codigo_udg + ")"),
					'asisTotales' : asistenciasTotales,
					'inasisTotales' : faltasTotales,
					'asisTCompleto' : asistenciasTC,
					'asisTMedio' : asistenciasTM,
					'inasisTMedio' : faltasTM,
					'inasisTCompleto' : faltasTC,
				})

				return render(request, 'Listas/estadisticas-profesor.html', locals())
				pass
			except:
				return redirect('/inicio-secretaria/')
		else:
			lista_profesores = Profesor.objects.all().order_by('apellido')
			objetos = "Profesores"
			form_size = 'small'
			return render(request, TEMPLATE_ESTADISTICAS_LISTAS, locals())
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def estadisticasMateria(request):
	if request.session['rol'] >= 1:
		if request.GET.get('materia'):
			materia = get_object_or_404(Materia, clave=request.GET.get('materia'))
			try:

				datos = {}
				tablamaterias = {}

				cicloActual = get_ciclo_vigente()

				if request.POST.get('fechaI','') and request.POST.get('fechaF',''):
					fechaI = request.POST.get('fechaI')
					fechaF = request.POST.get('fechaF')
					asistenciasTotales = Asistencia.objects.filter(
								fk_contrato__fk_curso__fk_ciclo__in=cicloActual,
								fk_contrato__fk_curso__fk_materia=materia,
								fecha__range=[fechaI , fechaF]
								)
					datos.update({
						'fechaI':fechaI,
						'fechaF':fechaF,
					})
				else:
					asistenciasTotales = Asistencia.objects.filter(
								fk_contrato__fk_curso__fk_ciclo__in=cicloActual,
								fk_contrato__fk_curso__fk_materia=materia
								)
				faltasTotales = asistenciasTotales.filter(asistio=False)
				profesoresTC = asistenciasTotales.filter(fk_contrato__tipo='T')
				profesoresTM = asistenciasTotales.filter(fk_contrato__tipo='P')

				valores = profesoresTC.values_list('fk_contrato__fk_curso__NRC',
												'fk_contrato__fk_tipocont__id').distinct()

				profesores = asistenciasTotales.values_list('fk_contrato__fk_curso__fk_profesor__codigo_udg',flat=True).distinct()
				#Filtrando valores repetidos
				for x in valores:
					profesoresTM = profesoresTM.exclude(fk_contrato__fk_curso__NRC=x[0],
													fk_contrato__fk_tipocont__id=str(x[1]))

				asistenciasTotales = profesoresTC | profesoresTM
				for key in profesores:
					if key not in tablamaterias:
						profesot_materia = Profesor.objects.get(codigo_udg = key)
						profesorAsistencias =  asistenciasTotales.filter(asistio=True,
											fk_contrato__fk_curso__fk_profesor__codigo_udg =key).count()
						profesorInasistencias =  asistenciasTotales.filter(asistio=False,
											fk_contrato__fk_curso__fk_profesor__codigo_udg =key).count()
						total = profesorAsistencias+profesorInasistencias
						if total == 0.0 : continue #Evitar que de error al intentar dividir entre 0
						asistenciasP = round(100 * float(profesorAsistencias)/float(total), 2)
						inasistenciasP = round(100 * float(profesorInasistencias)/float(total), 2)
						tablamaterias.update({str(key):
							{
							'maestro': profesot_materia.nombre + profesot_materia.apellido,
							'asistencias' : '%s(%s%%)'%(profesorAsistencias, asistenciasP),
							'inasistencias' :'%s(%s%%)'%(profesorInasistencias,inasistenciasP),
							'total' : total,
							}})
				datos.update({
					'nombre' : materia.nombre + " (" + materia.clave + ")",
					'asisTotales' : asistenciasTotales.count(),
					'inasisTotales' : faltasTotales.count(),
					'asisTCompleto' : profesoresTC.filter(asistio=True).count(),
					'asisTMedio' : profesoresTM.filter(asistio=True).count(),
					'inasisTCompleto' :  profesoresTC.filter(asistio=False).count(),
					'inasisTMedio' : profesoresTM.filter(asistio=False).count()
				})

				return render(request, 'Listas/estadisticas-materias.html', locals())
			except:
				return redirect('/inicio-secretaria/')
		else:
			form_size = 'small'
			objetos = "Materias"
			lista_materias = Materia.objects.all()
			return render(request, TEMPLATE_ESTADISTICAS_LISTAS, locals())     
	else:
		return redirect('error403', origen=request.path)
#Estadisticas de asistencia por ciclo escolar
@login_required(login_url='/')
def estadisticasCiclo(request):
	if request.session['rol'] >= 1:
		if request.GET.get('ciclo'):
			ciclo = get_object_or_404(Ciclo, id=request.GET.get('ciclo'))
			try:

				datos = {}
				tablaDepartamentos = {}

				if request.POST.get('fechaI','') and request.POST.get('fechaF',''):
					fechaI = request.POST.get('fechaI')
					fechaF = request.POST.get('fechaF')
					asistenciasTotales = Asistencia.objects.filter(fk_contrato__fk_curso__fk_ciclo=ciclo,
																fecha__range=[fechaI , fechaF])
					datos.update({
						'fechaI':fechaI,
						'fechaF':fechaF,
					})
				else:
					asistenciasTotales = Asistencia.objects.filter(fk_contrato__fk_curso__fk_ciclo=ciclo)

				departamentos = Departamento.objects.all()

				departamentosTC = asistenciasTotales.filter(fk_contrato__tipo='T')
				departamentosTM = asistenciasTotales.filter(fk_contrato__tipo='P')

				#Lista de valores para filtrar repetidos
				valores = departamentosTC.values_list('fk_contrato__fk_curso__NRC',
												'fk_contrato__fk_tipocont__id').distinct()

				#Filtrando valores repetidos
				for x in valores:
					departamentosTM = departamentosTM.exclude(fk_contrato__fk_curso__NRC=x[0],
													fk_contrato__fk_tipocont__id=str(x[1]))

				asistenciasTotales = departamentosTC | departamentosTM
				
				for x in departamentos:
					key = x.nick
					if key not in tablaDepartamentos:
						asistencias = asistenciasTotales.filter(asistio=True,
									fk_contrato__fk_curso__fk_materia__fk_departamento__nick=key).count()
						inasistencias = asistenciasTotales.filter(asistio=False,
									fk_contrato__fk_curso__fk_materia__fk_departamento__nick=key).count()
						total = asistencias + inasistencias
						tablaDepartamentos.update(
							{key:
								{
								'nombre':x.nombre,
								'asistencias':asistencias,
								'inasistencias':inasistencias,
								'total' : total
							}})

				#Aquí se genera la información que se pasará a la gráfica
				datos.update({
					'nombre' : "Ciclo " + ciclo.id,
					'asistenciasTotales' : asistenciasTotales.count(),
					'asistencias' : asistenciasTotales.filter(asistio=True).count(),
					'inasistencias' : asistenciasTotales.filter(asistio=False).count()
				})

				return render(request, 'Listas/estadisticas-ciclo.html', locals())
			except:
				return redirect('/inicio-secretaria/')
		else:
			objetos = "Ciclos"
			lista_ciclos = Ciclo.objects.all()
			form_size = 'small'
			return render(request, TEMPLATE_ESTADISTICAS_LISTAS, locals())
	else:
		return redirect('error403', origen=request.path)
