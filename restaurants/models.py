from django.db import models
from django.urls import reverse


class Restaurant(models.Model):
    name = models.CharField("Restauracja:",max_length=150)
    address = models.CharField("Adres:", max_length=255)
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
    name = models.CharField("Nazwa dania:", max_length=150)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=50)
    price = models.DecimalField("Cena:", max_digits=10, decimal_places=2)  # pole dla ceny
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restauracja:")  # Klucz obcy do modelu restauracja

    class Meta:
        verbose_name = "Posiłek"
        verbose_name_plural="Posiłki"

    def __str__(self):  # metoda do wyświetlania obiektu w django admin, dodajemy zł do pola ceny
        return '{} {}'.format(self.name, self. restaurant)


class FoodImage(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="food_images", blank=True)
    thumbnail = models.ImageField(upload_to="food-thumbnails", null=True)


