from django.db import models
from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import FileExtensionValidator

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(
        validators=[FileExtensionValidator(["jpg", "png"])], upload_to="imagenesPerfil")

    def __str__(self):
        return self.username

'''
class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    imagen_perfil = models.ImageField(validators=[FileExtensionValidator(["jpg", "png"])], upload_to="imagenesPerfil", default="")
    """Model definition for Usuario."""

    class Meta:
        """Meta definition for Usuario."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
'''

class Repositorio(models.Model):
    nombre = models.CharField(max_length=100)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Repositorio"""

        verbose_name = 'Repositorio'
        verbose_name_plural = 'Repositorios'

class Documento(models.Model):
    nombreDoc = models.CharField(max_length=100)
    fechaSubida = models.DateField(auto_now_add=True)
    fechaLimite = models.DateField()
    idRepositorio = models.ForeignKey(Repositorio, on_delete=models.CASCADE)
    documento = models.FileField(upload_to="documentos", validators=[
                                 FileExtensionValidator(["docx", "pdf"])])

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

class Permiso(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idDocumento = models.ForeignKey(Documento, on_delete = models.CASCADE)
    firmado = models.BooleanField()

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'



