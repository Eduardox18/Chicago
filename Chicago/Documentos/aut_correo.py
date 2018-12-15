from Documentos.models import Usuario
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(email=username)
            if check_password(password, usuario.password):
                return usuario
        except:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except:
            return None
