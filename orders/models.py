from django.core import exceptions
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from PIL import Image
from pyzbar.pyzbar import decode

from users.models import User, Address


from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from restaurants.models import Food

import logging

logger = logging.getLogger(__name__)


class Cart(models.Model):
    class Meta:
        verbose_name = "Koszyk"
        verbose_name_plural = "Koszyki"

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

    count.short_description = "Ilość: "

    def make_order(self, shipping_address):
        order_data = {
            "user": self.user,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "house_number": shipping_address.house_number,
            "flat_number": shipping_address.flat_number,
            "qr_code": shipping_address.qr_code,
        }
        order = Order.objects.create(**order_data)
        count = 0
        for line in self.cartline_set.all():
            for item in range(line.quantity):
                order_line_data = {
                    "order": order,
                    "product": line.food,
                }
                order_line = OrderLine.objects.create(**order_line_data)
                count += 1

        self.status = Cart.CartStatus.SUBMITTED
        self.save()
        return order_line

    def __str__(self):
        return 'Koszyk użytkownika {}'.format(self.user)


class CartLine(models.Model):
    '''
    Cart Queue
    '''
    class Meta:
        verbose_name = "Produkty w koszyku"
        verbose_name_plural = "Produkty w koszyku"

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Ilość:")
    total_price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)],
                                              verbose_name="Całkowita kwota zamówienia")

    '''def total_price(self):
        return self.quantity * self.food.price'''

    total_price.short_description = 'Koszt:'

    def __str__(self):
        return "Zamówienie :{}".format(self.food.name)


class Order(models.Model):
    class Meta:
        verbose_name = "zamówienie"
        verbose_name_plural = "Zamówienia"
        ordering = ['-date_placed']

    class OrderStatus(models.TextChoices):
        NEW = 'NOWE', _('Oczekuje na przyjęcie')
        PLACED = 'PRZYJĘTE', _('Zamówienie przyjęte.')
        COMPLETED = 'ZREALIZOWANE', _('Zamówienie zrealizowane')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Status zamówienia",
        max_length=15
    )
    '''
    Addresses are charfields, not foreign keys.
    Inside class Cart there's a defined method (make_order) which copies contents of address model
    That way if user deletes his addres, in order history there's still order to given address.
    '''
    shipping_address1 = models.CharField(max_length=60)
    shipping_address2 = models.CharField(max_length=60)
    house_number = models.CharField(max_length=60)
    flat_number = models.CharField(max_length=60, blank=True)
    qr_code = models.ImageField(upload_to="order_qrcodes", blank=True)

    date_updated = models.DateTimeField(auto_now=True)
    date_placed = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format(self.qr_code))

    def read_qr_code(self):
        '''
        https://www.programcreek.com/python/example/123813/pyzbar.pyzbar.decode
        :return:
        '''
        data = decode(Image.open(self.qr_code))
        return mark_safe(
            '<a href="{}" target="_blank">'
            '   <button class="submit-row" style= "cursor:pointer" type="button"> Nawiguj </button>'
            '</a>'.format(data[0].data.decode())
        )

    read_qr_code.short_description = 'Skanuj kod'
    image_tag.short_description = 'Kod QR'

    def __str__(self):
        return "ID zamówienia : {}".format(self.id)


class OrderLine(models.Model):
    NEW = 'NEW'
    ACCEPTED = 'ACCEPTED'
    BEING_PREPARED = 'BEING PREPARED'
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'
    STATUS = [
        (NEW, 'Oczekujące na przyjęcie'),
        (ACCEPTED, 'Zamówienie przyjęte'),
        (BEING_PREPARED, 'Zamówienie przygotowywane'),
        (SENT, 'Zamówienie wysłane'),
        (DELIVERED, 'Zamówienie dostarczone, zrealizowne'),
        (CANCELLED, 'Zamówienie anulowane'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Food, on_delete=models.PROTECT)  # if food deleted, order still in history
    status = models.CharField(choices=STATUS, default=NEW, max_length=15)

    def __str__(self):
        return "Zamówienie nr {}, {}".format(self.order_id, self.product.name)
