from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Usuario(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen_perfil = models.ImageField( validators=[FileExtensionValidator(["jpg", "png"])], upload_to="imagenesPerfil", default="")
    """Model definition for Usuario."""

    class Meta:
        """Meta definition for Usuario."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'



