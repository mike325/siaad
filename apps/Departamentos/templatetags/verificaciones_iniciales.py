# -*- coding: utf-8 -*-
'''
NOTA:
FAVOR DE UTILIZAR ESPACIOS COMO TABULACION.
El sistema de templatetags no funciona como el filtrado general
en el resto del codigo, donde no importa si se mezclan ambos.
También, tomar clara nota de la identación y los codigos de escape.
'''
import datetime
from django import template

from apps.Departamentos.models import *
from apps.Listas.models import *

register = template.Library()

@register.inclusion_tag('Departamentos/templatetags/verificacion.html', takes_context=True)
def advertencias_sist(context):
    hoy = datetime.date.today()

    problemas = True
    _verif_hayCiclos = Ciclo.objects.all().count()!=0
    _verif_hayCursos = Curso.objects.all().count()!=0
    _verif_hayDeptos = Departamento.objects.all().count()!=0
    _verif_hayContratos = Contrato.objects.all().count()!=0

    _ciclo_vigente = Ciclo.objects.filter(
            fecha_ini__lte=hoy,
            fecha_fin__gte=hoy
        )

    if _verif_hayCiclos \
        and _verif_hayDeptos \
        and _verif_hayCursos \
        and _verif_hayContratos \
        and _ciclo_vigente:
        problemas = False

    return {
            'problemas': problemas,
            'hayCiclos': _verif_hayCiclos,
            'hayDeptos': _verif_hayDeptos,
            'hayCursos': _verif_hayCursos,
            'cicloVigente': _ciclo_vigente,
            'hayContratos': _verif_hayContratos
        }