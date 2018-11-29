from django.forms import ModelForm, TextInput, FileInput, Textarea, forms,PasswordInput
from django.template.defaultfilters import filesizeformat
from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator 

class RegistroForm(ModelForm):
    password= forms.CharField(widget=PasswordInput())
    confirmar_password=forms.CharField(widget=PasswordInput())


    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = True
        self.fields['username'].max_length = 20
        self.fields['username'].error_messages = {'required': "Este campo es obligatorio."}
        self.fields['username'].help_text = 'Se utilizará este nombre de usuario para invitar a los demás a su repositorio.'

        self.fields['first_name'].required = True
        self.fields['first_name'].max_length = 20
        self.fields['first_name'].error_messages = {'required': "Este campo es obligatorio."}

        self.fields['last_name'].required = True
        self.fields['last_name'].max_length = 20
        self.fields['last_name'].error_messages = {'required': "Este campo es obligatorio."}

        self.fields['email'].required = True
        self.fields['email'].max_length = 50
        self.fields['email'].error_messages = {'required': "Este campo es obligatorio."}
        self.fields['email'].help_text = 'Se utilizará este correo electrónico para verificar su cuenta.'
        
    class Meta:
        """Meta definition for RegistroForm."""
        model = User
        fields = ('username', 'first_name','last_name','email','password')
    
    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden, deben ser iguales"
            )