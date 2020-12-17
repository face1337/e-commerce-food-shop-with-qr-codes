from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Cart, CartLine, Order
from restaurants.models import Food

from .forms import CartLineFormSet


def add_to_cart(request):
    food = get_object_or_404(Food, pk=request.GET.get('food_id'))
    cart = request.cart
    if not request.cart:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        cart = Cart.objects.create(user=user)
        request.session["cart_id"] = cart.id

    cartline, created = CartLine.objects.get_or_create(cart=cart, food=food)
    if not created:
        cartline.quantity += 1
        cartline.save()
    messages.info(
        request, "{} dodano do koszyka".format(food.name)
    )
    return HttpResponseRedirect(reverse('restaurants-foods', args=(food.restaurant.slug,)))


def manage_cart(request):
    if not request.cart:
        return render(request, 'orders/cart.html', {"formset": None})

    if request.method == "POST":
        formset = CartLineFormSet(request.POST, instance=request.cart)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/cart')
    else:
        formset = CartLineFormSet(instance=request.cart)

    if request.cart.is_empty():
        return render(request, 'orders/cart.html', {"formset": None})

    return render(request, 'orders/cart.html', {"formset": formset})


class StatisticsView(TemplateView):
    template_name = 'orders/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.values('city_district').annotate(Count("id")).order_by('-id__count')
        return context

