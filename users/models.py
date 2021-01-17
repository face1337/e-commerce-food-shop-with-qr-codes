from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)

import segno
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO

from django.utils.safestring import mark_safe
from geopy.geocoders import Nominatim


class UserManager(BaseUserManager):
    '''
    Menedżer napisany w celu nadpisania istniejącego modelu użytkownika
    '''
    use_in_migrations = True

    def _create_new_user(self, email, password, **extra_fields):
        '''
        metoda tworząca użytkownika, z której korzystają kolejne metody
        '''
        if not email:
            raise ValueError("Pole email nie może być puste")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_new_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser musi posiadać uprawnienia 'is_staff'"
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser musi posiadać uprawnienia 'is_superuser'"
            )
        return self._create_new_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('E-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserDeliveryInformation(models.Model):
    class Meta:
        verbose_name = "informacje o adresie"
        verbose_name_plural = "Adresy użytkowników"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    city = models.CharField("Miasto", max_length=60, default='Kraków', editable=False)
    street = models.CharField("Ulica", max_length=60)
    house_number = models.CharField("Nr bloku/domu", max_length=60)
    flat_number = models.CharField("Nr mieszkania", max_length=60, blank=True)
    city_district = models.CharField("Dzielnica", max_length=120, blank=True)
    country = models.CharField(max_length=60, default="Polska", editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        if self.flat_number is not None:
            return '{} {}/{}, {}, {} | {}'.format(self.street, self.house_number,
                                                  self.flat_number,self.city,
                                                  self.country, self.user)
        else:
            return '{} {}, {}, {} | {}'.format(self.street, self.house_number,
                                               self.city, self.country,
                                               self.user)

    def image_tag(self):
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format(self.qr_code))

    def read_qr_code(self):
        data = decode(Image.open(self.qr_code))
        return mark_safe(
            '<a href="{}" target="_blank">'
            '   <button class="submit-row" style= "cursor:pointer" type="button"> Nawiguj </button>'
            '</a>'.format(data[0].data.decode())
        )

    read_qr_code.short_description = 'Skanuj kod'
    image_tag.short_description = 'Kod QR'

    def get_address(self):
        return '{} {}, {}, {}'.format(self.street, self.house_number, self.city, self.country)

    def get_address_data(self):
        '''
        Metoda ta pobiera dane na podstawie wpisanego przez użytkownika adresu
        Następnie z tej metody można pobrać koordynaty
        :return: Informacje o adresie np. (Ulica, nr, dzielnica, miasto, lng, lat)
        '''
        geolocator = Nominatim(user_agent='users')
        location = geolocator.geocode(self.get_address(), addressdetails=True)
        return location

    def clean(self):
        '''
        Jeśli podany adres w formularzu jest nieprawidłowy, użytkownik dostanie błąd.
        '''
        coordinates = self.get_address_data()
        if coordinates is None:
            raise ValidationError("Podaj właściwy adres")

    def save(self, *args, **kwargs):
        latitude = self.get_address_data().latitude
        longitude = self.get_address_data().longitude
        buffer = BytesIO()
        qr_code_img = segno.make('https://www.google.pl/maps/place/{},{}'.format(latitude, longitude))
        qr_code_img.save(buffer, kind='png', light='#FFFFFF', scale=5)
        self.qr_code.save(f'{self.user}-qrcode.png', ContentFile(buffer.getvalue()), save=False)
        self.city_district = self.get_address_data().raw['address']['city_district']
        super().save(*args, **kwargs)
