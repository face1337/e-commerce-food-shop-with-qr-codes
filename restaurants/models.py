from django.db import models


class Restaurant(models.Model):
    """
    r_ stands for restaurant, so r_name means restaurant_name
    """
    r_name = models.CharField("Restauracja:",max_length=150)
    r_address = models.CharField("Adres:", max_length=255)

    def __str__(self):
        return '%s %s' % (self.r_name, self.r_address)


class Category(models.Model):
    """
    c_ stands for category, so c_name means category_name
    """
    c_name = models.CharField("Kategoria:", max_length=150)

    def __str__(self):
        return '%s' % self.c_name


class Food(models.Model):
    """
    f_ stands for food, so f_name means food_name
    """
    f_name = models.CharField("Nazwa dania:", max_length=150)
    f_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria:")  # Klucz obcy do kategorii jedzenia
    f_price = models.DecimalField("Cena:", max_digits=10, decimal_places=2)  # pole dla ceny
    f_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restauracja:")  # Klucz obcy do modelu restauracja

    def __str__(self):  # metoda do wyświetlania obiektu w django admin, dodajemy zł do pola ceny
        return '%s %s %s' % (self.f_name, self.f_category, self.f_restaurant) + " " + str(self.f_price) + " zł"



