from django.shortcuts import render, redirect
from Documentos.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django import forms
from django.http import JsonResponse
from .models import *

def ingresar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/documentos/')
        else:
            return render(request, "login.html")
    
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/documentos/')
        else:
            return render(request, 'documentos.html', {'mensaje':'error'})

def registrar(request):
    if request.method == 'GET':
        form = CrearUsuarioForm(use_required_attribute=False)
        return render(request, 'registro.html', {'form':form})
    elif request.method == 'POST':
        form = CrearUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'form':form})
        else:
            print("no jaló")
            form = CrearUsuarioForm(request.POST)
            return render(request, 'registro.html',{'form':form})

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
    permisos = Permiso.objects.filter(idUsuario = request.user)
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
    elif request.method =='DELETE':
        usuario = User.objects.get(username = request.user.username)
        print(usuario.username)
        usuario.is_active = False
        usuario.save()
        logout(request)
        return redirect('/login/')
    else:
        form = ModificarUsuarioForm(instance=request.user)
        return render(request, "cuenta.html", {"form": form})

def borrar_usuario(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(username=request.user.username)
        print(usuario.username)
        usuario.is_active = False
        usuario.save()
        logout(request)
        return redirect('/login/')


def crear_repositorio(request):
    repositorioForm = RepositorioForm()

    if request.method == "GET":
        return render(request,"registro_repositorio.html", {'form':repositorioForm})
    if request.method == "POST":
        repositorioForm = RepositorioForm(request.POST)
        if repositorioForm.is_valid():
            repositorioForm.instance.idUsuario = request.user
            repositorioForm.save()

            return redirect("/repositorios/")
        else:
            return render(request,'registro_repositorio.html',{'form':repositorioForm})

@transaction.atomic
def crear_documento(request):
    documentoForm = DocumentoForm()

    if request.method == "GET":
        return render (request, "registro_documento.html", {'form': documentoForm})
    elif request.method == "POST":
        documentoForm = DocumentoForm(request.POST, request.FILES)
        if documentoForm.is_valid():
            #Recupera el nombre de archivo y lo separa de la extensión
            nombre_archivo = request.FILES["documento"].name.split(".")
            documentoForm.instance.nombreDoc = nombre_archivo[0]
            documentoForm.save()
            id_documento = Documento.objects.latest("id")
            permiso = Permiso(idUsuario=request.user, idDocumento=id_documento, esPropietario = True, firmado = False)
            permiso.save()
            return redirect("/documentos")
        else:
            context = {'form': documentoForm, 'mensaje': 'error'}
            return render(request,'registro_documento.html', context)

def mostrar_chat(request):
    return render(request, "chat.html")

def mandar_mensaje(request, destinatario, mensaje):
    if request.method == "POST":
        try:
            chat = Chat(idUsuarioRemitente=request.user.id, idUsuarioDestinatario = destinatario, mensaje = mensaje)
            chat.save()
            data = {"resultado": True}
        except:
            data = {"resultado": False}

        return JsonResponse(data)

def salir(request):
    logout(request)
    return redirect('/login/')
