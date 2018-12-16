from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from Documentos.models import *


class CrearUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Usuario
        fields = ["username", "first_name", "last_name",
                  "email", "imagen_perfil"]

class ModificarUsuarioForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = Usuario
        fields = ["username", "first_name", "last_name",
                  "email", "imagen_perfil"]

class DocumentoForm(ModelForm):

    class Meta:
        model = Documento
        fields = (
            "documento",
            "fechaLimite"
        )
