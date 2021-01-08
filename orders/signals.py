from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart


@receiver(user_logged_in)
def merge_cart_from_session(sender, user, request, **kwargs):
    session_cart = getattr(request, "cart", None)
    if session_cart:
        try:
            new_cart_for_logged_user = Cart.objects.get(user=user, status=Cart.OPEN)
            for line in session_cart.cartline_set.all():
                line.cart = new_cart_for_logged_user
                line.save()
            session_cart.delete()
            request.cart = new_cart_for_logged_user
            new_cart_for_logged_user.save()
        except Cart.DoesNotExist:
            session_cart.user = user
            session_cart.save()
