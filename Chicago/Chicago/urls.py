"""Chicago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Documentos.views import *
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url,include

urlpatterns = [
    path('login/', ingresar),
    path('registro/', registrar),
    path('index/', login_required(abrir_home)),
    path('logout/', salir),
    path('repositorios/', login_required(mostrar_repositorios)),
    path('info/', mostrar_info),
    path('delete/', login_required(borrar_usuario)),
    path('cuenta/', login_required(cuenta_usuario)),
    path('crearRepositorio/', login_required(crear_repositorio)),
    path('documentos/<int:id_repo>', login_required(mostrar_documentos)),
    path('crearDocumento/<int:id_repo>', login_required(crear_documento))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]