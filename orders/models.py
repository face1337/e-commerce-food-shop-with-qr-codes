from django.db import models
from django.utils import timezone
from users.models import User


from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from restaurants.models import Food


class Cart(models.Model):

    class CartStatus(models.TextChoices):
        OPEN = 'NOWY', _('Nowy koszyk')
        SUBMITTED = 'WYSŁANY', _('Wysłany')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik:", blank=True, null=True)
    status = models.CharField(max_length=15, choices=CartStatus.choices, default=CartStatus.OPEN)
    date_placed = models.DateTimeField(default=timezone.now)

    def is_empty(self):
        return self.cartline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.cartline_set.all())

    def __str__(self):
        return '{}'.format(self.user)


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Ilość:")

    def __str__(self):
        return "Zamówienie :{}".format(self.food.name)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'NOWE', _('Utworzono nowe zamówienie')
        PLACED = 'ZŁOŻONE', _('Zamówienie przyjęte')
        BEING_PREPARED = 'PRZYGOTOWYWANIE', _('Zamówienie przygotowywane')
        SENT = 'WYSŁANE', _('Zamówienie wysłane')
        COMPLETED = 'ZREALIZOWANE', _('Zamówienie zrealizowane')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Status zamówienia",
        max_length=15
    )

    phone_number = models.DecimalField(verbose_name="Numer telefonu", max_digits=9, decimal_places=0)
