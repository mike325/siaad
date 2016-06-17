# -*- coding: utf-8 -*-
'''CAMPOS PARA SUPLENTES'''
FieldSet_Suplente = []
FieldSet_Suplente.append({
		'label': 'NRC',
		'id': 'in-nrc',
		'value': 'fk_curso.NRC',
		'send': False,
		'disable': True,
		'size': 2
	})
FieldSet_Suplente.append({
		'label': 'Clave',
		'id': 'in-cvemat',
		'value': 'fk_curso.fk_materia.clave',
		'send': False,
		'disable': True,
		'size': 2
	})
FieldSet_Suplente.append({
		'label': 'Materia',
		'id': 'in-materia',
		'value': 'fk_curso.fk_materia.nombre',
		'send': False,
		'disable': True,
		'size': 8
	}) # break
FieldSet_Suplente.append({
		'label': 'SECC',
		'id': 'in-secc',
		'value': 'fk_curso.fk_secc',
		'send': False,
		'disable': True,
		'max_length': 5,
		'size': 2
	})
FieldSet_Suplente.append({
		'label': 'Profesor',
		'id': 'in-profesor',
		'value': 'fk_curso.fk_profesor',
		'send': False,
		'disable': True,
		'size': 5
	}) # break
FieldSet_Suplente.append({
		'label': 'Suplente',
		'id': 'in-supp',
		'send': False,
		'value': 'fk_profesor',
		'rel': 'in-codigo',
		'size': 5
	}) # break
FieldSet_Suplente.append({
		'id': 'in-codigo',
		'type': 'hidden',
		'value': 'fk_profesor.codigo_udg',
		'set': 'fk_profesor',
		'model': 'Profesor',
		'filter': 'codigo_udg',
		'size': 0
	})
FieldSet_Suplente.append({
		'rootclass': 'rango-fecha',

		'label': 'Inicio suplencia',
		'id': 'in-periodo-ini',
		'class': 'date start',
		'value': 'periodo_ini',
		'set': 'periodo_ini',
		'prop': 'date',
		'size': 3
	})
FieldSet_Suplente.append({
		'rootclass': 'rango-fecha',

		'label': 'Fin suplencia',
		'id': 'in-periodo-fin',
		'class': 'date end',
		'value': 'periodo_fin',
		'set': 'periodo_fin',
		'prop': 'date',
		'size': 3
	})
FieldSet_Suplente.append({
		'rootclass': 'end',
		'rootstyle': 'padding-top: 27px;',

		'checklabel': 'Vigente todo el ciclo.',
		'id': 'in-full-periodo',
		'type': 'checkbox',
		'special': { 'periodo_ini': None, 'periodo_fin': None },
		'value': 'periodo_fin==None',
		'rel': 'in-periodo-ini, in-periodo-fin',
		'size': 3
	})

'''CAMPOS PARA CICLOS'''
FieldSet_Ciclo = []
FieldSet_Ciclo.append({
		'label': 'Nombre ciclo',
		'id': 'in-id-ciclo',
		'value': 'id',
		'set': 'id',
		'max_length': 6,
		'size': 4
	})
FieldSet_Ciclo.append({
		'label': 'Fecha inicio',
		'id': 'in-ciclo-ini',
		'value': 'fecha_ini',
		'set': 'fecha_ini',
		'class': 'date start',
		'prop': 'date',
		'size': 4
	})
FieldSet_Ciclo.append({
		'label': 'Fecha fin',
		'id': 'in-ciclo-fin',
		'value': 'fecha_fin',
		'set': 'fecha_fin',
		'class': 'date end',
		'prop': 'date',
		'size': 4
	})

'''CAMPOS PARA PROFESORES'''
FieldSet_Profesor = []
FieldSet_Profesor.append({
		'label': 'Codigo UDG',
		'id': 'in-codigo',
		'value': 'codigo_udg',
		'send': False,
		'disable': True,
		'size': 3
	})
FieldSet_Profesor.append({
		'label': 'Apellidos',
		'id': 'in-apellido',
		'value': 'apellido',
		'max_length': 50,
		'set': 'apellido',
		'rtrim': True,
		'size': 4
	})
FieldSet_Profesor.append({
		'label': 'Nombre(s)',
		'id': 'in-nombre',
		'value': 'nombre',
		'max_length': 50,
		'set': 'nombre',
		'rtrim': True,
		'size': 5
	})