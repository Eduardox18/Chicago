from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm, PasswordInput
from Documentos.models import *


class CrearUsuarioForm(UserCreationForm):
    clave_certificado = forms.CharField(widget=PasswordInput())

    class Meta(UserCreationForm):
        model = Usuario
        fields = ["username", "first_name", "last_name",
                  "email", "imagen_perfil", "clave_certificado"]
        
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
