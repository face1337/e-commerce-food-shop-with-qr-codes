from django.db import models
from django.utils import timezone
from users.models import User

from django.utils.translation import gettext_lazy as _
from restaurants.models import Restaurant, Food  # zaimportowanie modelu restauracji


'''class Order(models.Model):

    class OrderStatus(models.TextChoices):
        NONE = 'BRAK', _('Nie złożono zamówienia')
        PLACED = 'ZŁOŻONE', _('Zamówienie przyjęte')
        BEING_PREPARED = 'PRZYGOTOWYWANIE', _('Zamówienie przygotowywane')
        SENT = 'WYSŁANE', _('Zamówienie wysłane')
        COMPLETED = 'ZREALIZOWANE', _('Zamówienie zrealizowane')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik:")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restauracja:")
    product = models.ManyToManyField(Food, through='FoodInOrder')
    date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.NONE)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    comments = models.TextField(blank=True, verbose_name="Uwago do zamówienia: ")
    # delivery_time = models.TimeField(verbose_name="Czas dostawy: ")  # not sure if needed

    def __str__(self):
        return "Zamówienie: {}".format(self.product)


class FoodInOrder(models.Model):
    # Represent information about specific food product ordered by customer
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Food, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
'''