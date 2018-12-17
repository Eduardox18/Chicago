from django import forms
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import FileExtensionValidator
from django.db import models

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(
        validators=[FileExtensionValidator(["jpg", "png"])], upload_to="imagenesPerfil")
    clave_certificado = models.CharField(max_length=100)
    certificado = models.TextField(max_length=200, blank=True, null=True, default=None)

    def __str__(self):
        return self.username

class Documento(models.Model):
    nombreDoc = models.CharField(max_length=100)
    fechaSubida = models.DateField(auto_now_add=True)
    fechaLimite = models.DateField()
    documento = models.FileField(upload_to="documentos", validators=[
                                 FileExtensionValidator(["docx", "xlsx", "pdf"])])
    imagen_documento = models.ImageField(
        validators=[FileExtensionValidator(["jpg", "png"])], upload_to="imagenesDocumento", default="")

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

class Permiso(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idDocumento = models.ForeignKey(Documento, on_delete = models.CASCADE)
    firmado = models.BooleanField()
    esPropietario = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

class Chat(models.Model):
    idUsuarioRemitente = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='remitente')
    idUsuarioDestinatario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='destinatario')
    mensaje = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

class Notificacion(models.Model):
    idUsuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='usuario')
    idRemitente = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='emisor')
    idDocumento = models.ForeignKey(
        Documento, on_delete = models.CASCADE, blank = True, null = True, default = None)
    idMensaje = models.ForeignKey(
        Chat, on_delete=models.CASCADE, blank=True, null=True, default=None)
    visto = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'
