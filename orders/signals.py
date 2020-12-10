from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart


@receiver(user_logged_in)
def merge_carts_if_found(sender, user, request, **kwargs):
    anonymous_cart = getattr(request, "cart", None)
    if anonymous_cart:
        try:
            logged_in_cart = Cart.objects.get(user=user, status=Cart.OPEN)
            for line in anonymous_cart.cartline_set.all():
                line.cart = logged_in_cart
                line.save()
            anonymous_cart.delete()
            request.cart = logged_in_cart
            logged_in_cart.save()
        except Cart.DoesNotExist:
            anonymous_cart.user = user
            anonymous_cart.save()
