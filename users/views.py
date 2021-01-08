from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages

from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from users import forms
from .forms import AddressForm, SelectAddressForm
from .models import Address
from orders.models import OrderLine, Order


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = forms.UserCreationForm

    def get(self, request, *args, **kwargs): # jeśli zalogowany użytkownik spróbuję dostać się na stronę rejestracji, zostanie przekierowany
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('restaurants-index'))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()  # zapisanie użytkownika
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(
            self.request, "Zarejestrowano pomyślnie."
        )
        return response


class MyLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('restaurants-index'))
        return super().get(request, *args, **kwargs)


class ListOfAddressesView(LoginRequiredMixin, ListView):
    model = Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CreateNewAddressView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'users/address_form.html'

    form_class = AddressForm

    success_url = reverse_lazy("users-address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = [
        "address2",
        "house_number",
        "flat_number",
    ]
    success_url = reverse_lazy("users-address_list")
    template_name = 'users/address_update.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy("users-address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class SelectAddressView(LoginRequiredMixin, FormView):
    template_name = 'users/address_select.html'
    form_class = SelectAddressForm
    success_url = reverse_lazy('restaurants-list')

    def get_form_kwargs(self):
        '''
        extract the user form
        :return: return user in dict
        '''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['cart_id']  # if form is valid, delete items in cart
        cart = self.request.cart
        cart.user = self.request.user
        cart.make_order(form.cleaned_data['address'])
        messages.info(
            self.request, "Pomyślnie złożono zamówienie. Aby sprawdzić jego status przejdź do zakładki 'zamówienia'."
        )

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.cart is None or self.request.cart.count() == 0:
            return HttpResponseRedirect(reverse('restaurants-index'))
        return super().get(request, *args, **kwargs)


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ItemsInOrderListView(LoginRequiredMixin, ListView):
    model = OrderLine
    template_name = 'orders/order_details.html'
    context_object_name = 'order_details'

    def get_queryset(self):
        order = get_object_or_404(Order, id=self.kwargs.get('pk'))
        return self.model.objects.filter(order_id=order)

