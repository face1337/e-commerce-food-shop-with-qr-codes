from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from PIL import Image
from pyzbar.pyzbar import decode

from users.models import User, Address
from restaurants.models import Food


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

    def get_total_price(self):
        return sum(i.food.price*i.quantity for i in self.cartline_set.all())

    count.short_description = "Ilość: "

    def make_order(self, shipping_address):
        order_data = {
            "user": self.user,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "house_number": shipping_address.house_number,
            "flat_number": shipping_address.flat_number,
            "qr_code": shipping_address.qr_code,
            "city_district": shipping_address.city_district,
            "total_price": self.get_total_price(),
        }
        order = Order.objects.create(**order_data)
        count = 0
        for line in self.cartline_set.all():
            for item in range(line.quantity):
                order_line_data = {
                    "order": order,
                    "product": line.food,
                    "price": line.food.price,
                }
                order_line = OrderLine.objects.create(**order_line_data)
                count += 1
        self.status = Cart.CartStatus.SUBMITTED
        self.save()
        return order_line

    def __str__(self):
        return 'Koszyk użytkownika {}'.format(self.user)


class CartLine(models.Model):
    class Meta:
        verbose_name = "Produkty w koszyku"
        verbose_name_plural = "Produkty w koszyku"

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Ilość:")
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=None)

    total_price.short_description = 'Koszt:'

    def __str__(self):
        return "Zamówienie :{}".format(self.food.name)


class Order(models.Model):
    '''
    Addresses are charfields, not foreign keys.
    Inside class Cart there's a defined method (make_order) which copies contents of address model
    That way if user deletes his addres, in order history there's still order to given address.
    '''
    class Meta:
        verbose_name = "zamówienie"
        verbose_name_plural = "Zamówienia"
        ordering = ['-date_placed']

    class OrderStatus(models.TextChoices):
        NEW = 'NOWE', _('Oczekuje na przyjęcie')
        PLACED = 'PRZYJĘTE', _('Zamówienie przyjęte.')
        BEING_PREPARED = 'PRZYGOTOWYWANE', _('W trakcie przygotowania')
        SENT = 'WYSŁANE', _('Zamówienie wysłane')
        COMPLETED = 'ZREALIZOWANE', _('Zamówienie dostarczone, zrealizowane')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Status zamówienia",
        max_length=15
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Suma")
    shipping_address1 = models.CharField(max_length=60, verbose_name="Miasto")
    shipping_address2 = models.CharField(max_length=60, verbose_name="Ulica")
    house_number = models.CharField(max_length=60, verbose_name="Nr domu")
    flat_number = models.CharField(max_length=60, blank=True, verbose_name="Nr mieszkania")
    qr_code = models.ImageField(upload_to="order_qrcodes", blank=True, verbose_name="Kod QR")
    city_district = models.CharField(max_length=120, blank=True, verbose_name="Dzielnica")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")
    date_placed = models.DateTimeField(auto_now_add=True, verbose_name="Data złożenia zamówienia")

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
    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Food, on_delete=models.PROTECT, default=1, verbose_name="Produkt")  # if food deleted, order still in history
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Koszt")

    def __str__(self):
        return "Zamówienie nr {}, {}".format(self.order_id, self.product.name)
