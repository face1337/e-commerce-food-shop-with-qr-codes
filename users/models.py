from django.db import models
from django.contrib.auth.models import User
from qr_code.qrcode.utils import Coordinates
from qr_code.qrcode import *
from io import BytesIO
from django.core.files import File
from PIL import Image
import segno
from geopy.geocoders import Nominatim
from qr_code.templatetags.qr_code import qr_for_google_maps


class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField("Adres (Ulica nr domu/mieszkania, miejscowość, kraj:", max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, max_length=1000)

    def __str__(self):
        return 'Profil użytkownika: {}'.format(self.name)

    def get_coordinates(self):
        '''
        Convert given address to coordinates, used later on for google maps
        :return: location in coordinates (ex. 49.0215125, 50.434124)
        '''
        geolocator = Nominatim(user_agent="users")
        location = geolocator.geocode(self.address)
        return location

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        google_maps_coordinates = Coordinates(latitude=self.get_coordinates().latitude,
                                              longitude=self.get_coordinates().longitude)

        qr_code_img = qr_for_google_maps(coordinates=google_maps_coordinates)
        fname = f'qr-{self.name}.png'
        self.qr_code.save(qr_code_img, fname, save=False)
        """
        To powyżej nie działa, dostaje error - "SuspiciousFileOperation at /admin/users/profile/7/change/
        Storage can not find an available filename for... "
        Zwiększone max_length dla qr_code ale nadal się to dzieje.
        """
        # img.close()



