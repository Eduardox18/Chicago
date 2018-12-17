from Crypto.PublicKey import RSA
from django.conf import settings

class Generator:
    def generate_key(username):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        ruta = settings.MEDIA_ROOT + "/certificados/" + "private_key_" + username + ".pem"

        with open (ruta, "w") as prv_file:
            print("{}".format(private_key.exportKey()), file=prv_file)

        return ruta
