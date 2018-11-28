from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Usuario(models.Model):
    def get_upload_path(instance, filename):    
        return os.path.join("%s" % imagenPerfil, "%s" %instance.usuario.username, "%s" % filename)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen_perfil = models.FileField( validators=[FileExtensionValidator(["docx", "pdf"])], upload_to="media/imagenesPerfil/", max_length=100)
    """Model definition for Usuario."""

    class Meta:
        """Meta definition for Usuario."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.usuario.username



