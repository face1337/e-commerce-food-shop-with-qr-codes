from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.core.files import File

import qrcode
from PIL import Image
from io import BytesIO
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


class Profile(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField("Adres (Ulica nr domu/mieszkania, miejscowość, kraj:", max_length=255, default='adres')
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
