# Similar a django.shortcuts, pretende proveer de metodos y clases
# utiles y/o automatizar procesos largos que tienden a repetirse
# a lo largo de todo el codigo.

from functools import wraps
from django.shortcuts import render, redirect
from apps.Departamentos.models import Departamento, Ciclo
from apps.Usuarios.models import Usuario

import datetime

def panelInicio(request):
    if request.user.is_authenticated():
        if request.session['rol'] == 1:
            return redirect('inicio_secretaria')
        elif request.session['rol'] == 2:
            return redirect('inicio_jefedep')
        else:
            return redirect('inicio_admin')
    else:
        return redirect('/')

def sidebar_context(request):
    return{
        'lista_departamentos' : Departamento.objects.all(),
    }

# def ciclo_context(request):
#     hoy = datetime.date.today()
#     context_ciclo_vig = Ciclo.objects.filter(
#         fecha_ini__lte=hoy,
#         fecha_fin__gte=hoy
#     )
#     return { 'context_cicloVigente': context_ciclo_vig }

def verifica_dpto(origen):
    '''
        FIX:
            + Limpieza de la funcion.
            + Ahora se evalua correctamente si existe el dpto en
              las variables de la solicitud.
            + Ahora se redirige a la pagina de "no-autorizado" si
              el usuario no tiene el permiso suficiente.
    '''
    @wraps(origen)
    def wrapper(request, *args, **kwargs):
        error = False
        if 'dpto' in kwargs and request.session['usuario']['rol'] <= 2:
            _verif_usuario = request.user.username
            _verif_usuario = Usuario.objects.get(user__username=_verif_usuario)

            _verif_departamento = None
            try:
                _verif_departamento = Departamento.objects.get(nick=kwargs['dpto'])
                pass
            except:
                # Muy probablemente se haya generado una consulta equivocada
                # (el departamento no existe o algun error por lo parecido)
                # pero dejemos el procesamiento de dicho error al sistema.
                # aka: "dejemoslo pasar"
                pass

            if _verif_departamento and _verif_departamento.jefeDep != _verif_usuario:
                error = True

                pass

            _verif_departamento = None
            _verif_usuario = None
            pass # if

        if error:
            return redirect('error403', origen=request.path)

        return origen(request, *args, **kwargs)
        pass #wrapper()
    return wrapper

def get_ciclo_vigente():
    hoy = datetime.date.today()
    return Ciclo.objects.filter(
            fecha_ini__lte=hoy,
            fecha_fin__gte=hoy
        )