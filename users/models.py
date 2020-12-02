from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.core.files import File

import qrcode
from PIL import Image
from io import BytesIO

from django.utils.safestring import mark_safe
from geopy.geocoders import Nominatim


class UserManager(BaseUserManager):
    '''
    Creating own user model, users will use email, not username.
    '''
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff set to True"
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser set to True"
            )
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('E-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Address(models.Model):
    class Meta:
        verbose_name_plural = "Adresy użytkowników"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik:")
    address1 = models.CharField("Miasto:", max_length=60, default='Kraków', editable=False)  # locked for Kraków
    address2 = models.CharField("Ulica:", max_length=60)
    house_number = models.CharField("Nr bloku/domu:", max_length=60)
    flat_number = models.CharField("Nr mieszkania:", max_length=60, blank=True)
    country = models.CharField(max_length=60, default="Polska", editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, max_length=3000)

    def __str__(self):
        return '{}'.format(self.user)

    def image_tag(self):
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format(self.qr_code))

    image_tag.short_description = 'Kod QR'

    def get_address(self):
        if self.flat_number is not None:
            return '{} {}/{}, {}, {}'.format(self.address2, self.house_number,
                                             self.flat_number, self.address1,self.country)
        else:
            return '{} {}, {}, {}'.format(self.address2, self.house_number,
                                          self.address1, self.country)

    def get_coordinates(self):
        '''
        Convert given address to coordinates, used later on for google maps
        :return: location in coordinates (ex. 49.0215125, 50.434124)
        '''
        geolocator = Nominatim(user_agent='users')
        location = geolocator.geocode(self.get_address())
        return location

    def clean(self):
        coordinates = self.get_coordinates()
        if coordinates is None:
            raise ValidationError("Podaj właściwy adres")

    def save(self, *args, **kwargs):
        latitude = self.get_coordinates().latitude
        longitude = self.get_coordinates().longitude
        qr_code_img = qrcode.make('https://www.google.pl/maps/place/{},{}'.format(latitude, longitude))
        img = Image.new('RGB', (qr_code_img.pixel_size, qr_code_img.pixel_size), color='white')
        img.paste(qr_code_img)
        fname = f'qr-{self.user}.png'
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        img.close()

        super().save(*args, **kwargs)
