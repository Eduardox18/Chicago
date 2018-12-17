from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url,include    
app_name="Documentos"

urlpatterns = [
    path('login/', ingresar),
    path('registro/', registrar),
    path('logout/', salir),
    path('info/', mostrar_info),
    path('delete/', login_required(borrar_usuario)),
    path('cuenta/', login_required(cuenta_usuario)),
    path('documentos/', login_required(mostrar_documentos)),
    path('crearDocumento/', login_required(crear_documento)),
    path('principalDocumento/<int:id_doc>', login_required(ir_principal_documento)),
    path('deleteDocumento/<int:id_doc>', login_required(borrar_documento)),
    path('chat/<str:username>', login_required(mostrar_chat)),
    path('enviarMensaje/', mandar_mensaje),
    path('usuarios/', ajax_recuperar_usuarios),
    path('recuperarMesajes/', ajax_recuperar_mensajes),
    path('notificaciones/', ajax_recuperar_notificaciones),
    path('verNotificacion/<int:id_notif>/<str:tipo>/<str:clave>', ajax_ver_notificacion),
    
    #confirmación de cuentas 
    path('activate<uid>/<token>', activate, name="activate"),
    
]