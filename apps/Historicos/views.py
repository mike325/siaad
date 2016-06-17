# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.Historicos.models import Registro
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import re

from apps.Departamentos.models import *
from SistemaAdministrativo.commons.shortcuts import *

TEMPLATE_HISTORICOS = 'Historicos/historicos.html'

@login_required(login_url="/")
@verifica_dpto
def historicos(request, dpto):
    if request.session['rol'] >= 2:
        dpto = Departamento.objects.get(nick=dpto)
        registros = Registro.objects.filter(
                        Q(fk_departamento__nick=dpto.nick) | 
                        Q(fk_departamento=None)).order_by("-fechaHoraModificacion")
        paginator = Paginator(registros, 50)
        pagina = request.GET.get('pagina')

        try:
            registros = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            registros = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            registros = paginator.page(paginator.num_pages)
            
        return render(request, TEMPLATE_HISTORICOS, locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url="/")
@verifica_dpto
def historicosFiltrados(request, dpto):
    if request.session['rol'] >= 2:
        if request.method == 'POST':
            dpto = Departamento.objects.get(nick=dpto)
            fecha = request.POST.get('fecha','')
            fecha_expr = re.compile('[\d]{4}-[\d]{2}-[\d]{2}')
            res = fecha_expr.match(fecha)
            if res:
                registros = Registro.objects.filter(
                                fk_departamento__nick=dpto.nick,
                                fechaHoraModificacion__startswith=fecha
                                ).order_by("-fechaHoraModificacion")
                paginator = Paginator(registros, 50)
                pagina = request.GET.get('pagina')
                try:
                    registros = paginator.page(pagina)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    registros = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    registros = paginator.page(paginator.num_pages)
                return render(request, TEMPLATE_HISTORICOS, locals())
            else:
                registros = Registro.objects.all().order_by("-fechaHoraModificacion")
                errors = "Ingresa una fecha válida"
                return render(request, TEMPLATE_HISTORICOS, locals())
        else:
            return redirect('/historicos/')
    else:
        return redirect('error403', origen=request.path)