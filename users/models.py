from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField("Adres:", max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
