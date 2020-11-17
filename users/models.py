from django.db import models
from django.contrib.auth.models import User
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File
from geopy.geocoders import Nominatim


class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField("Adres (Ulica nr domu/mieszkania, miejscowość, kraj:", max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, max_length=3000)

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
        latitude = self.get_coordinates().latitude
        longitude = self.get_coordinates().longitude

        qr_code_img = qrcode.make('https://www.google.pl/maps/place/{},{}'.format(latitude, longitude))
        img = Image.new('RGB', (qr_code_img.pixel_size, qr_code_img.pixel_size), color='white')
        img.paste(qr_code_img)
        fname = f'qr-{self.name}.png'
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        img.close()

        super().save(*args, **kwargs)



