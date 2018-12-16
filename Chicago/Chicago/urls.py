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
    path('logout/', salir),
    path('info/', mostrar_info),
    path('delete/', login_required(borrar_usuario)),
    path('cuenta/', login_required(cuenta_usuario)),
    path('crearRepositorio/', login_required(crear_repositorio)),
    path('documentos/', login_required(mostrar_documentos)),
    path('crearDocumento/', login_required(crear_documento)),
    path('principalDocumento/<int:id_doc>', login_required(ir_principal_documento)),
    path('deleteDocumento/<int:id_doc>', login_required(borrar_documento)),
    path('chat/<str:username>', login_required(mostrar_chat)),
    path('enviarMensaje/', mandar_mensaje),
    path('usuarios/', ajax_recuperar_usuarios),
    path('recuperarMesajes/', ajax_recuperar_mensajes),
    path('notificaciones/', ajax_recuperar_notificaciones),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
