from django.shortcuts import render, redirect
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
            user = authenticate(username=usuario.username, password=password)
            login(request, user)
            return redirect('/documentos/')
        else:
            return render(request, 'login.html', {'mensaje': 'error'})


def registrar(request):
    if request.method == 'GET':
        form = CrearUsuarioForm(use_required_attribute=False)
        return render(request, 'registro.html', {'form': form})
    elif request.method == 'POST':
        form = CrearUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'form': form})
        else:
            print("no jaló")
            form = CrearUsuarioForm(request.POST)
            return render(request, 'registro.html', {'form': form})


def abrir_home(request):
    return render(request, "documentos.html")


'''
def mostrar_repositorios(request):
    if request.method == "GET":
        repositorios = Repositorio.objects.filter(idUsuario = request.user)
        context = {'repositorios': repositorios}
        return render(request, "repositorios.html", context)
'''


def mostrar_documentos(request):
    permisos = Permiso.objects.filter(idUsuario=request.user)
    ids = []
    for permiso in permisos:
        ids.append(permiso.idDocumento.id)
    documentos = Documento.objects.filter(pk__in=ids)
    context = {"documentos": documentos}
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


def crear_repositorio(request):
    repositorioForm = RepositorioForm()

    if request.method == "GET":
        return render(request, "registro_repositorio.html", {'form': repositorioForm})
    if request.method == "POST":
        repositorioForm = RepositorioForm(request.POST)
        if repositorioForm.is_valid():
            repositorioForm.instance.idUsuario = request.user
            repositorioForm.save()

            return redirect("/repositorios/")
        else:
            return render(request, 'registro_repositorio.html', {'form': repositorioForm})


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

    if request.method == "GET":
        info = {}
        info["esPropietario"] = permiso.esPropietario
        info["documento"] = documento
        context = {'info': info}
        return render(request, 'principal_documento.html', context)


def mostrar_chat(request, username):
    if request.method == "GET":
        usuario = Usuario.objects.get(username=username)
        context = {"username": usuario.username, "id": usuario.id}
        return render(request, "chat.html", context)


def mandar_mensaje(request):
    if request.method == "POST":
        destinatario = request.POST.get("destinatario")
        id_destinatario = Usuario.objects.get(username=destinatario)
        mensaje = request.POST.get("mensaje")

        try:
            chat = Chat(idUsuarioRemitente=request.user,
                        idUsuarioDestinatario=id_destinatario, mensaje=mensaje)
            chat.save()
            data = {"resultado": True}
        except:
            print("error")
            data = {"resultado": False}

        return JsonResponse(data)


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

def salir(request):
    logout(request)
    return redirect('/login/')
