from django.db import models
from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import FileExtensionValidator

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(
        validators=[FileExtensionValidator(["jpg", "png"])], upload_to="imagenesPerfil")

    def __str__(self):
        return self.username

class Documento(models.Model):
    nombreDoc = models.CharField(max_length=100)
    fechaSubida = models.DateField(auto_now_add=True)
    fechaLimite = models.DateField()
    documento = models.FileField(upload_to="documentos", validators=[
                                 FileExtensionValidator(["pdf"])])
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

class Notificacion(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idDocumento = models.ForeignKey(Documento, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'

class Chat(models.Model):
    idUsuarioRemitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='remitente')
    idUsuarioDestinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destinatario')
    mensaje = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'



