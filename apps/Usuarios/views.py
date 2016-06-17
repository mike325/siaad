# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from SistemaAdministrativo.commons.shortcuts import *

from apps.Departamentos.models import Departamento
from apps.Usuarios.models import Usuario, Rol
from apps.Historicos.models import Registro

# las plantillas que se llamen mas de una vez es mejor ponerlas como constantes
TEMPLATE_ALTA_JEFEDEP = 'Usuarios/nuevo-jefeDep.html'
TEMPLATE_ALTA_SECRE = 'Usuarios/nueva-secretaria.html'
TEMPLATE_MODIFICA_PASS = 'Usuarios/modificar-password.html'

def login(request):
    if request.method == 'POST':
        #Tomar los valores mandados al hacer log in
        usuario = request.POST.get('username','')
        password = request.POST.get('pass','')
        
        #Autentificar que el usuario exista
        user = auth.authenticate(username=usuario, password=password)

        #Si el usuario existe  y está activo, se inicia la sesión
        if user is not None and user.is_active:
            auth.login(request, user)

            usuario = Usuario.objects.get(user=user)
            usuario = {
                    'nick': usuario.user.username,
                    'correo': usuario.user.email,
                    'nombre': usuario.user.first_name,
                    'apellidos': usuario.user.last_name,
                    'codigo': usuario.codigo,
                    'rol': usuario.rol.id
                }

            #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
            request.session['usuario'] = usuario
            request.session['rol'] = user.usuario.rol.id
            request.session['just_logged'] = True

            return panelInicio(request)
        else:
            return render(request,'Usuarios/login.html', {'errors': "Usuario o contraseña incorrectos"})
    else:
        if request.user.is_authenticated():
            return panelInicio(request)
        else:
            return render(request, 'Usuarios/login.html')

def logout(request):
    try:
        auth.logout(request)
    except KeyError:
        pass
    return redirect('/')

#Verificar si el usuario está logeado, en caso contrario, redirecciona a página de log in
@login_required(login_url='/')
def inicio_admin(request):
    #revisa que el usuario tenga permisos necesarios para ver el contenido de esta página
    departamentos = Departamento.objects.all()
    if request.session['rol'] == 3:
        banner = True
        bienvenida = False

        if request.session['just_logged']:
            bienvenida = True
            request.session['just_logged'] = False
            
        departamentos = Departamento.objects.all()
        return render(request, 'inicio-administrador.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def sistema_modificar_jefedep(request, dpto):
    if request.session['rol'] == 3:
        form_size = 'small'
        if request.method == 'POST':
            #Tomar valores del POST
            post_jefeActual = request.POST.get('jefeActual', '')
            post_departamento = request.POST.get('departamento', '')
            post_nuevoJefe = request.POST.get('nuevoJefe', '')

            #¿Qué hacer con el antiguo jefe de departamento?
            username_jefeActual = post_jefeActual.split(",",1)[0]
                
            #Query del objeto del nuevo jefe
            nuevoJefe = Usuario.objects.get(user__username = post_nuevoJefe)

            #Query del departamento del jefe actual
            departamento = Departamento.objects.get(nombre = post_departamento)

            #Sustitución del jefe actual por el nuevo
            nuevoJefe.hacer_jefe()
            departamento.jefeDep = nuevoJefe

            #Guardar los cambios en la base de datos
            departamento.save()

            dpto = Departamento.objects.get(nick=dpto)

            try:
                jefeActual = Usuario.objects.get(user__username=username_jefeActual)
            except ObjectDoesNotExist:
                registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creo el jefe del departamento "'+
                        post_departamento+'" "'+nuevoJefe.user.get_full_name()+'"',
                        nuevoJefe, 'Departamentos', dpto)
                registro.save()
                return redirect('/inicio-administrador/')
            registro = Registro.modificacion(request.session['usuario']['nick'],
                        'Se cambio el jefe del departamento "'+
                        post_departamento+'" de "'+jefeActual.user.get_full_name()+
                        '" a "'+nuevoJefe.user.get_full_name()+'"', jefeActual,
                        nuevoJefe, 'Departamentos', dpto)
            registro.save()
            return redirect('/inicio-administrador/')
        else:
            if Departamento.objects.filter(nick=dpto).exists():
                errors = ""
                try:
                    departamento = Departamento.objects.get(nick=dpto)
                    jefeActual = departamento.jefeDep
                    opcionesJefeDepartamento = Usuario.objects.filter(user__is_active=True, rol__id__gte=1, departamento=None)
                except ObjectDoesNotExist:
                    errors = "No existen jefes de este departamento, favor de crear uno."
                return render(request, 'Forms/modificar-jefe-departamento.html', locals())
            else:
                return redirect('/inicio-administrador/')
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def nuevo_departamento(request):
    if request.session['rol'] == 3:
        form_size = 'small'
        #Revisar si se entra a la página por POST
        if request.method == 'POST':
            #Obtener los campos del nuevo departamento
            post_abreviacion = request.POST.get('abreviacion','')
            post_nombre = request.POST.get('nombre', '')
            post_nuevoJefe = request.POST.get('nuevoJefe', '')
            
            #Hacer query del nuvo jefe
            nuevoJefe = Usuario.objects.get(user__username=post_nuevoJefe)

            #Crear el nuevo departamento
            nuevoDepartamento = Departamento(nick=post_abreviacion, nombre=post_nombre, jefeDep=nuevoJefe)
            
            #Guardar en la base de datos el nuevo departamento
            nuevoDepartamento.save()

            dpto = Departamento.objects.get(nick=post_abreviacion)
            registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creo el departamento "'+post_nombre+'"'
                        , post_nombre, 'Departamentos', dpto)
            registro.save()

            return redirect('/inicio-administrador/')

        #Si no se entra con POST, se regresa el formulario de nuevo departamento
        else:
            opcionesJefeDepartamento = Usuario.objects.filter(user__is_active=True, rol__id__gte=1, departamento=None)
            return render(request, 'Forms/nuevo-departamento.html', {
                                                'opcionesJefeDepartamento':opcionesJefeDepartamento,
                                                'form_size':form_size,
                                                })
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def nuevo_jefe(request):
    if request.session['rol'] == 3:
        form_size = 'small'

        if request.method == 'POST':
            usuario = request.POST.get('username','')
            password = request.POST.get('password', '')
            codigo = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')
            
            if User.objects.filter(Q(username=usuario) | Q(email=correo)).exists():
                
                errors = 'Ya existe registro con ese nombre'
                return render(request, TEMPLATE_ALTA_JEFEDEP, locals())
            else:
                nuevo_usuario = Usuario.alta_jefe(usuario, password, nombre, 
                                                    apellido, correo, codigo)
                nuevo_usuario.save()
                try:
                    dpto = Departamento.objects.get(jefeDep=nuevo_usuario)
                    registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creo el jefe de departamento "'
                        + nuevo_usuario.user.get_full_name() +'"',
                        usuario, 'Usuarios', dpto)
                except:
                    registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creo el jefe de departamento "'
                        + nuevo_usuario.user.get_full_name() +'"',
                        usuario, 'Usuarios', None)
                registro.save()

                return redirect('/inicio-administrador/')
        else:
            return render(request, TEMPLATE_ALTA_JEFEDEP, locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def nueva_secretaria(request):
    if request.session['rol'] >= 2:
        form_size = 'small'

        if request.method == 'POST':
            usuario = request.POST.get('username','')
            password = request.POST.get('password', '')
            codigo = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')

            if User.objects.filter(Q(username=usuario) | Q(email=correo)).exists():

                errors = 'Ya existe registro con ese nombre'
                return render(request, TEMPLATE_ALTA_SECRE, locals())
            else:
                nuevo_usuario = Usuario.alta_secretaria(usuario, password, nombre, 
                                                    apellido, correo, codigo)
                nuevo_usuario.save()

                registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creo la secretaria "'+nuevo_usuario.user.get_full_name()+'"'
                        , usuario, 'Usuarios', None)
                registro.save()

                return redirect('/')
        else:
            return render(request, TEMPLATE_ALTA_SECRE, locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def activar_usuarios(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            usuarios = Usuario.objects.exclude(user__username = 'admin').order_by('user__username')

            for x in usuarios:
                estado = request.POST.get(x.user.username,'')

                if estado=='active' and not x.user.is_active:
                    x.user.is_active = True
                    registro = Registro.modificacion(request.session['usuario']['nick'],
                            'Se activo el usuario "'+
                            x.user.username +'"', 'Inactivo',
                            'Activo', 'Usuarios', None)
                    x.user.save()
                    registro.save()
                elif estado=='unactive' and x.user.is_active:
                    x.user.is_active = False
                    registro = Registro.modificacion(request.session['usuario']['nick'],
                            'Se desactivo el usuario "'+
                            x.user.username +'"', 'Activo',
                            'Inactivo', 'Usuarios', None)
                    x.user.save()
                    registro.save()

            return redirect('/')
        else:
            usuarios = Usuario.objects.exclude(user__username = 'admin').order_by('user__username')
            return render(request, 'Usuarios/activar-usuarios.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def modificar_perfil(request):
    if request.session['rol'] >= 1: # basicamente cualquier usuario, no? e.e

        form_size = 'small'
        user_modificar = request.session['usuario']['nick']
        correo_modificar = request.session['usuario']['correo']
        perfil = Usuario.objects.get(user__username = user_modificar)

        if request.method == 'POST':
            usuario1 = request.POST.get('username','')
            codigo1 = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')
            modificar = Usuario.objects.filter(user__username = user_modificar).update(codigo = codigo1)

            if not User.objects.exclude(username=request.session['usuario']['nick']).filter(email=correo).exists():
                modificar_user = User.objects.filter(username = request.session['usuario']['nick']).update(
                                                first_name = nombre,
                                                last_name = apellido, email = correo)
                usuario = Usuario.objects.get(user__username = request.session['usuario']['nick'])
                usuario = {
                        'nick': usuario.user.username,
                        'correo': usuario.user.email,
                        'nombre': usuario.user.first_name,
                        'apellidos': usuario.user.last_name,
                        'codigo': usuario.codigo,
                        'rol': usuario.rol.id
                    }
                #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
                request.session['usuario'] = usuario
                request.session['just_logged'] = True
                return panelInicio(request)
            else:
                errors = "Ya esta siendo usado ese correo"
                return render(request, 'Usuarios/modificar-perfil.html', locals())
        else:
            return render(request, 'Usuarios/modificar-perfil.html', locals())        
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def modificar_password(request):
    if request.session['rol'] >= 1:
        form_size = 'small'

        if request.method == 'POST':
            password_actual = request.POST.get('password_actual','')
            password_nuevo = request.POST.get('password_nuevo','')
            verificacion_password = request.POST.get('verificacion_password','')
            #Autentificar que el usuario exista
            user_actual = request.session['usuario']['nick']
            usuario = User.objects.get(username=user_actual)
            #Si el usuario existe  y está activo, cambia contrase~a
            if password_nuevo == verificacion_password:
                usuario.set_password(password_nuevo)
                usuario.save()
                user = auth.authenticate(username=user_actual, password=password_nuevo)
                #Si el usuario existe  y está activo, se inicia la sesión
                auth.login(request, user)
                usuario = Usuario.objects.get(user=user)
                usuario = {
                        'nick': usuario.user.username,
                        'correo': usuario.user.email,
                        'nombre': usuario.user.first_name,
                        'apellidos': usuario.user.last_name,
                        'codigo': usuario.codigo,
                        'rol': usuario.rol.id
                    }
                #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
                request.session['usuario'] = usuario
                request.session['rol'] = user.usuario.rol.id
                request.session['just_logged'] = True
                return redirect ('/inicio-administrador/')
            else:
                errors = "Confirmacion de contraseña erronea"
                return render(request, TEMPLATE_MODIFICA_PASS, locals())
        else:
            return render(request, TEMPLATE_MODIFICA_PASS, locals())
    else:
        return redirect('error403', origen=request.path)
