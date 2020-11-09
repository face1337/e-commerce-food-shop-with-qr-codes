from django.db import models


class Restaurant(models.Model):
    name = models.CharField("Restauracja:",max_length=150)
    address = models.CharField("Adres:", max_length=255)

    def __str__(self):
        return '{} {} '.format(self.name, self.address)


class Category(models.Model):
    name = models.CharField("Kategoria:", max_length=150)

    def __str__(self):
        return '{}'.format(self.name)


class Food(models.Model):
    name = models.CharField("Nazwa dania:", max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria:")  # Klucz obcy do kategorii jedzenia
    price = models.DecimalField("Cena:", max_digits=10, decimal_places=2)  # pole dla ceny
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restauracja:")  # Klucz obcy do modelu restauracja

    def __str__(self):  # metoda do wyświetlania obiektu w django admin, dodajemy zł do pola ceny
        return '{} {} {} {} zł'.format(self.name, self.category, self. restaurant, self.price)



