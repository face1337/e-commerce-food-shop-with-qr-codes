from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from restaurants.models import Restaurant  # zaimportowanie modelu restauracji


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        NONE = 'BRAK', _('Nie złożono zamówienia')
        PLACED = 'ZŁOŻONE', _('Zamówienie przyjęte')
        BEING_PREPARED = 'PRZYGOTOWYWANIE', _('Zamówienie przygotowywane')
        SENT = 'WYSŁANE', _('Zamówienie wysłane')
        COMPLETED = 'ZREALIZOWANE', _('Zamówienie zrealizowane')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik:")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restauracja:")
    date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.NONE)
    # delivery_time = models.TimeField(verbose_name="Czas dostawy: ")  # not sure if needed
