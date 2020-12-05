from django.contrib.auth import signals
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import logging

from .models import Cart

logger = logging.getLogger(__name__)


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
            logger.info("Dodano do koszyka dla {}".format(user),)
            logged_in_cart.save()
        except Cart.DoesNotExist:
            anonymous_cart.user = user
            anonymous_cart.save()
            logger.info(
                "Przypisano użytkownika do koszyka id {}".format(anonymous_cart.id,)
            )