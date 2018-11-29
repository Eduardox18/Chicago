from django.shortcuts import render, redirect
from Documentos.forms import RegistroForm, EditarForm
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
        form = RegistroForm(use_required_attribute=False)
        return render(request, 'registro.html', {'form':form})
    elif request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            email = request.POST.get('email',None)
            password = request.POST.get('password', None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            try:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                return render(request, 'login.html', {'form':form})
            except:
                return render(request, 'registro.html', {'form':'Formulario completado'})
        else:
            form = RegistroForm(request.POST)
            return render(request, 'registro.html',{'form':form})

def abrir_home(request):
    return render(request, "index.html")

def mostrar_repositorios(request):
    return render(request, "repositorios.html")

def mostrar_info(request):
    return render(request, "info.html")

def cuenta_usuario(request):
    if request.method == 'GET':
        form = EditarForm(use_required_attribute=False)
        return render(request, 'cuenta.html', {'form': form})
    elif request.method == "PUT":
        form = EditarForm(request.PUT)
        if form.is_valid():
            username = request.PUT.get('username', None)
            email = request.PUT.get('email', None)
            password = request.PUT.get('password', None)
            first_name = request.PUT.get('first_name', None)
            last_name = request.PUT.get('last_name', None)
            try:
                usuario = User.objects.get(pk = id)
                usuario.username = username
                usuario.email = email
                usuario.first_name = first_name
                usuario.last_name = last_name
                usuario.save()
                return redirect('/index/')
            except:
                return render(request, 'cuenta.html', {'form': 'Formulario completado'})
        else:
            form = EditarForm(request.PUT)
            return render(request, 'cuenta.html', {'form': form})



def salir(request):
    logout(request)
    return redirect('/login/')
