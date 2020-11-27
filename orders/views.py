from django.shortcuts import render


def shopping_cart(request, template_name='orders/shopping_cart.html'):
    cart = get_shopping_cart(request)
    context = {'cart': cart}
    return render_to_response
