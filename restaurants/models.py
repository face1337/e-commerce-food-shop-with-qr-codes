from django.core.files.base import ContentFile
from django.db import models
from django.utils.safestring import mark_safe

import segno
# from pyzbar.pyzbar import decode
from io import BytesIO


class Restaurant(models.Model):
    name = models.CharField("Restauracja:",max_length=150)
    address = models.CharField("Adres:", max_length=255)
    city = models.CharField("Miasto:", max_length=150, default="Kraków")
    slug = models.SlugField("URL:",max_length=50)

    class Meta:
        verbose_name = "Restauracja"
        verbose_name_plural = "Restauracje"

    def __str__(self):
        return '{} {} '.format(self.name, self.address)


class Category(models.Model):
    name = models.CharField("Kategoria:", max_length=150)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField("Nazwa dania", max_length=150)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=50)
    price = models.DecimalField("Cena", max_digits=10, decimal_places=2)  # pole dla ceny
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restauracja")  # Klucz obcy do modelu restauracja
    description = models.TextField(blank=True, max_length=500)
    # kalorie i ig (cukier dla cukrzyków)
    calories = models.CharField(blank=True, max_length=50, verbose_name='Kalorie')
    ig = models.CharField(blank=True, max_length=50, verbose_name='Indeks glikemiczny')
    # kod qr dla informacji powyżej
    qr_code = models.ImageField(upload_to='food_qr_codes', blank=True)

    class Meta:
        verbose_name = "Posiłek"
        verbose_name_plural="Posiłki"

    def __str__(self):  # metoda do wyświetlania obiektu w django admin, dodajemy zł do pola ceny
        return '{} {}'.format(self.name, self. restaurant)

    def save(self, *args, **kwargs):
        buffer = BytesIO()
        qr_code_img = segno.make(f'Kalorie: {self.calories}, Indeks glikemiczny: {self.ig}')
        qr_code_img.save(buffer, kind='png', light='#FFFFFF', scale=4)
        self.qr_code.save(f'{self.name}-qrcode.png', ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)


class FoodImage(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="Posiłek")
    image = models.ImageField(upload_to="food_images", blank=True, verbose_name="Obraz")
    thumbnail = models.ImageField(upload_to="food-thumbnails", blank=True, null=True, verbose_name="Miniatura")

    class Meta:
        verbose_name ="Obraz produktu"
        verbose_name_plural = "Obrazy produktu"

    def image_tag(self):
        return mark_safe('<img src="/media/{}"/>'.format(self.image))

    image_tag.short_description = 'Obraz'

    def __str__(self):
        return self.food.name