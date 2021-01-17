from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.mail import send_mail

from PIL import Image
from pyzbar.pyzbar import decode

from users.models import User, UserDeliveryInformation
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

    def make_order(self, address):
        data_for_order_model = {
            "user": self.user,
            "city": address.city,
            "street": address.street,
            "house_number": address.house_number,
            "flat_number": address.flat_number,
            "qr_code": address.qr_code,
            "city_district": address.city_district,
            "total_price": self.get_total_price(),
        }
        order = Order.objects.create(**data_for_order_model)
        products = []
        for line in self.cartline_set.all():
            for item in range(line.quantity):
                items = {
                    "order": order,
                    "product": line.food,
                    "price": line.food.price,
                }
                order_line = OrderLine.objects.create(**items)
                products.append(line.food.name)
        message = 'Dziękujemy za złożenie zamówienia. \n' \
                  'Produkty które zamówiłeś to: \n \n' \
                  '   -'

        message += '\n   -'.join(products)
        message += f'\n \n Wartość zamówienia: {self.get_total_price()} zł'
        message += '\n \n Studentzamawia.pl'
        send_mail(
            f'Zamówienie użytkownika {self.user}',
            message,
            'administracja@studentzamawia.pl',
            [self.user],
            fail_silently=True,
        )
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
    Adresy zostały zdefiniowane jako pola typu CharField, a nie klucz obcy, ponieważ metoda modelu Cart make_order(),
    kopiuje informacje pól z modelu UserDeliveryInformation. Dzięki temu, jeśli użytkownik usunie swój adres dostawy, historia
    zamówienia nadal posiada podany ówczas adres.
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

    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Użytkownik", null=True)
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Status zamówienia",
        max_length=15
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Suma")
    city = models.CharField(max_length=60, verbose_name="Miasto")
    street = models.CharField(max_length=60, verbose_name="Ulica")
    house_number = models.CharField(max_length=60, verbose_name="Nr domu")
    flat_number = models.CharField(max_length=60, blank=True, verbose_name="Nr mieszkania")
    qr_code = models.ImageField(upload_to="order_qrcodes", blank=True, verbose_name="Kod QR")
    city_district = models.CharField(max_length=120, blank=True, verbose_name="Dzielnica")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")
    date_placed = models.DateTimeField(auto_now_add=True, verbose_name="Data złożenia zamówienia")

    def image_tag(self):
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format(self.qr_code))

    def read_qr_code(self):
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

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Food, on_delete=models.PROTECT, default=1, verbose_name="Produkt")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Koszt")

    def __str__(self):
        return "Zamówienie nr {}, {}".format(self.order_id, self.product.name)
