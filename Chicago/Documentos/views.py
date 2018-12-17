from django.shortcuts import render, redirect, HttpResponse, Http404, get_object_or_404
from Documentos.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models import Q
from django import forms
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
import hashlib
from .generator import *


def ingresar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/documentos/')
        else:
            return render(request, "login.html")

    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            usuario = None

        if usuario is not None:
            if usuario.is_active:
                user = authenticate(username=usuario.username, password=password)
                login(request, user)
                return redirect('/documentos/')
            else:
                return render(request, 'login.html', {'mensaje': 'success'})
        else:
            return render(request, 'login.html', {'mensaje': 'error'})


def registrar(request):
    if request.method == 'GET':
        form = CrearUsuarioForm(use_required_attribute=False)
        return render(request, 'registro.html', {'form': form})
    elif request.method == 'POST':
        form = CrearUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.is_active=False
            instance.clave_certificado = hashlib.sha256(instance.clave_certificado.encode()).hexdigest()
            instance.save()
            site=get_current_site(request)
            email = request.POST.get('email', None)
            #envio de mensaje de confirmación send_mail(subject, message, from_email, to_list, fail_silentry=True)
            subject='Confirmación de cuenta Chicago'
            message=render_to_string('confirm_email.html', {
                "user":instance,
                "domain":site.domain,
                "uid":instance.id,
                "token":activation_token.make_token(instance)
            })
            to_list=[email]
            from_email=settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            #return HttpResponse ("<h1>Gracias por registrarte, el correo de confirmación fue enviado a tu email</h1>")
            return render(request, 'login.html', {'form': form, 'mensaje':'success'})
        else:
            print("no jaló")
            form = CrearUsuarioForm(request.POST)
            return render(request, 'registro.html', {'form': form})


def activate(request, uid, token):
    try:
        usuario=get_object_or_404(Usuario,pk=uid)
    except:
        raise Http404("No se encontró el usuario")
    if usuario is not None and activation_token.check_token(usuario,token):
        usuario.is_active=True
        ruta_certificado = Generator.generate_key(usuario.username)
        usuario.certificado = ruta_certificado
        usuario.save()
        return HttpResponse ("<h2>Cuenta activada. Ahora puedes iniciar sesión haciendo <a href='/login'>click aquí</a></h2>")
    else:
        return HttpResponse ("<h3>Link de activación inválido</h3>")


def abrir_home(request):
    return render(request, "documentos.html")

def mostrar_documentos(request):
    permisos = Permiso.objects.filter(idUsuario=request.user, esPropietario = True)
    ids = []
    for permiso in permisos:
        ids.append(permiso.idDocumento.id)
    documentos = Documento.objects.filter(pk__in=ids)

    permisos = Permiso.objects.filter(idUsuario=request.user, esPropietario = False)
    ids = []
    for permiso in permisos:
        ids.append(permiso.idDocumento.id)
    documentosCompartidos = Documento.objects.filter(pk__in=ids)
    usuarios = Usuario.objects.exclude(username = request.user.username)
    

    info = {}
    info["documentos"] = documentos
    info["documentosCompartidos"] = documentosCompartidos
    info["usuarios"] = usuarios

    context = {"info": info}
    return render(request, "documentos.html", context)

def mostrar_info(request):
    return render(request, "info.html")

def cuenta_usuario(request):
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/cuenta/')
    elif request.method == 'DELETE':
        usuario = User.objects.get(username=request.user.username)
        print(usuario.username)
        usuario.is_active = False
        usuario.save()
        logout(request)
        return redirect('/login/')
    else:
        form = ModificarUsuarioForm(instance=request.user)
        return render(request, "cuenta.html", {"form": form})

def borrar_usuario(request):
    usuario = Usuario.objects.get(username=request.user.username)
    usuario.is_active = False
    usuario.save()
    logout(request)
    return redirect('/login/')

def borrar_documento(request, id_doc):
    documento = Documento.objects.get(id=id_doc)
    documento.delete()
    return redirect('/documentos/')

@transaction.atomic
def crear_documento(request):
    documentoForm = DocumentoForm()

    if request.method == "GET":
        return render(request, "registro_documento.html", {'form': documentoForm})
    elif request.method == "POST":
        documentoForm = DocumentoForm(request.POST, request.FILES)
        if documentoForm.is_valid():
            # Recupera el nombre de archivo y lo separa de la extensión
            nombre_archivo = request.FILES["documento"].name.split(".")
            documentoForm.instance.nombreDoc = nombre_archivo[0]
            documentoForm.save()
            id_documento = Documento.objects.latest("id")
            permiso = Permiso(
                idUsuario=request.user, idDocumento=id_documento, esPropietario=True, firmado=False)
            permiso.save()
            return redirect("/documentos")
        else:
            context = {'form': documentoForm, 'mensaje': 'error'}
            return render(request, 'registro_documento.html', context)

def ir_principal_documento(request, id_doc):
    permiso = Permiso.objects.get(idUsuario=request.user, idDocumento=id_doc)
    documento = Documento.objects.get(id=id_doc)

    falta_firmar = Permiso.objects.filter(idDocumento = id_doc, firmado = False)
    usuarios = []

    for permiso in falta_firmar:
        usuarios.append(permiso.idUsuario.first_name)

    if request.method == "GET":
        info = {}
        info["esPropietario"] = permiso.esPropietario
        info["documento"] = documento
        info["usuarios"] = usuarios
        context = {'info': info}
        return render(request, 'principal_documento.html', context)

def mostrar_chat(request, username):
    if request.method == "GET":
        usuario = Usuario.objects.get(username=username)
        nombre = usuario.first_name + " " + usuario.last_name
        context = {
            "username": usuario.username, 
            "id": usuario.id, 
            "nombre": nombre}
        return render(request, "chat.html", context)

def mandar_mensaje(request):
    if request.method == "POST":
        destinatario = request.POST.get("destinatario")
        id_destinatario = Usuario.objects.get(pk=destinatario)
        mensaje = request.POST.get("mensaje")

        try:
            chat = Chat(idUsuarioRemitente=request.user,
                        idUsuarioDestinatario=id_destinatario, mensaje=mensaje)
            chat.save()
            data = {"resultado": True}
        except:
            data = {"resultado": False}

        return JsonResponse(data)

def ir_firmar_documento(request, id_documento):
    firmarForm = FirmarForm()

    if request.method == "GET":
        return render(request, 'firmar.html', {'form': firmarForm})
    elif request.method == "POST":
        firmarForm = FirmarForm(request.POST, request.FILES)
        if firmarForm.is_valid():
            archivo = request.FILES["llave"]
            data_enviada = archivo.read()
            clave = request.POST["clave_archivo"]
            usuario = Usuario.objects.get(id = request.user.id)

            with open('./media/certificados/private_key_' + usuario.username + '.pem', 'rb') as myfile:
                data_guardada = myfile.read()
            
            permisos = Permiso.objects.filter(idUsuario=request.user, esPropietario = True)
            ids = []
            for permiso in permisos:
                ids.append(permiso.idDocumento.id)
            documentos = Documento.objects.filter(pk__in=ids)

            permisos = Permiso.objects.filter(idUsuario=request.user, esPropietario = False)
            ids = []
            for permiso in permisos:
                ids.append(permiso.idDocumento.id)
            documentosCompartidos = Documento.objects.filter(pk__in=ids)
            usuarios = Usuario.objects.exclude(username = request.user.username)
            

            info = {}
            info["documentos"] = documentos
            info["documentosCompartidos"] = documentosCompartidos
            info["usuarios"] = usuarios
            info["id_documento"] = id_documento

            cifrada = hashlib.sha256(clave.encode()).hexdigest()

            if (data_enviada == data_guardada and usuario.clave_certificado == cifrada):
                permiso = Permiso.objects.get(idUsuario = request.user, idDocumento = id_documento)
                permiso.firmado = True
                permiso.save()
                info["mensaje"] = 'firmado'
                context = {'info': info}
                return render(request, "documentos.html", context)
            else:
                info["mensaje"] = 'noFirmado'
                context = {'form': firmarForm, 'info': info}
                return render(request, "documentos.html", context)
        else:
            context = {'form': firmarForm, 'mensaje': 'error'}
            return render(request, 'firmar.html', context)

@csrf_exempt
def ajax_recuperar_usuarios(request):
    usuarios_disponibles = serializers.serialize(
        "json", Usuario.objects.exclude(id=request.user.id))
    return JsonResponse({"lista": usuarios_disponibles})

@csrf_exempt
def ajax_recuperar_mensajes(request):
    destinatario = request.POST.get("destinatario")
    remitente = request.user.id
    mensajes_recuperados = Chat.objects.filter(
        Q(idUsuarioRemitente=remitente) & Q(idUsuarioDestinatario=destinatario) | Q(idUsuarioDestinatario=remitente) & Q(idUsuarioRemitente=destinatario))
    mensajes = serializers.serialize("json", mensajes_recuperados)
    return JsonResponse({"mensajes": mensajes})

@csrf_exempt
def ajax_ver_notificacion(request, id_notif, tipo, clave):
    notificacion = Notificacion.objects.get(pk=id_notif)
    notificacion.visto = True
    notificacion.save()

    if tipo == "mensaje":
        return mostrar_chat(request, clave)
    else:
        return ir_principal_documento(request, int(clave))


@csrf_exempt
def ajax_recuperar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(idUsuario=request.user.id, visto=False)
    notif_usuarios = []
    for notificacion in notificaciones:
        if notificacion.idDocumento == None:
            notif_usuarios.append(
                {
                    "id": notificacion.id,
                    "remitente": notificacion.idRemitente.first_name,
                    "userRemitente": notificacion.idRemitente.username,
                    "idMensaje": notificacion.idMensaje.id,
                    "mensaje": notificacion.idMensaje.mensaje,
                    "idDocumento": "",
                    "nombreDoc": "",
                }
            )
        else:
            notif_usuarios.append(
                {
                    "id": notificacion.id,
                    "remitente": notificacion.idRemitente.first_name,
                    "userRemitente": notificacion.idRemitente.username,
                    "idMensaje": "",
                    "mensaje": "",
                    "idDocumento": notificacion.idDocumento.id,
                    "nombreDoc": notificacion.idDocumento.nombreDoc,
                }
            )
    return JsonResponse({"notificaciones": notif_usuarios})

@csrf_exempt
def ajax_compartir_documento(request):
    diccionario = json.loads(request.POST.get("values"))
    lista_usuarios = diccionario["lista_usuarios"]
    documento = diccionario["id_documento"]

    for usuario in lista_usuarios:
        recuperado = Usuario.objects.get(id = int(usuario))
        try:
            verificar = Permiso.objects.get(
                idUsuario=recuperado, idDocumento=documento)
        except Permiso.DoesNotExist:
            verificar = None
            
        if verificar is not None:
            permiso = Permiso(idUsuario = recuperado, idDocumento = documento, firmado = False, esPropietario = False)
            permiso.save()
            notificacion = Notificacion(idUsuario = recuperado, idRemitente = request.user, idDocumento = documento, visto = False)
            notificacion.save()
    
    return JsonResponse({"documento": 1})

def salir(request):
    logout(request)
    return redirect('/login/')
