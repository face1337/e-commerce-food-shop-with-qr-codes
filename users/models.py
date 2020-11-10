from django.db import models
from django.contrib.auth.models import User
import qr_code
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField("Adres:", max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return 'Profil użytkownika: {}'.format(self.name)

    #TODO: save method for generating a qr code based on given address

