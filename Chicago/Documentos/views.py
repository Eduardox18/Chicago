from django.shortcuts import render, redirect
from Documentos.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms

def ingresar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/index/')
        else:
            return render(request, "login.html")
    
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/index/')
        else:
            return render(request, 'login.html', {'mensaje':'error'})

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
    return render(request, "index.html")

def mostrar_repositorios(request):
    if request.method == "GET":
        repositorios = Repositorio.objects.filter(idUsuario = request.user)
        context = {'repositorios': repositorios}
        return render(request, "repositorios.html", context)

def mostrar_documentos(request, id_repo):
    documentos = Documento.objects.filter(idRepositorio = id_repo)
    nombre_repo = Repositorio.objects.get(id = id_repo)
    id_repo = nombre_repo.id
    nombre_repo = nombre_repo.nombre
    context = {"documentos": documentos, "nombre_repo": nombre_repo, "id_repo": id_repo}
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
        usuario = User.objects.get(username=request.user.username)
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

def crear_documento(request, id_repo):
    documentoForm = DocumentoForm()

    if request.method == "GET":
        return render (request, "registro_documento.html", {'form': documentoForm})
    elif request.method == "POST":
        documentoForm = DocumentoForm(request.POST, request.FILES)
        if documentoForm.is_valid():
            #Recupera el nombre de archivo y lo separa de la extensión
            nombre_archivo = request.FILES["documento"].name.split(".")
            documentoForm.instance.nombreDoc = nombre_archivo[0]
            documentoForm.instance.idRepositorio_id = id_repo
            documentoForm.save()
            return redirect("/documentos/"+str(id_repo))
        else:
            context = {'form': documentoForm, 'mensaje': 'error'}
            return render(request,'registro_documento.html', context)

def salir(request):
    logout(request)
    return redirect('/login/')
