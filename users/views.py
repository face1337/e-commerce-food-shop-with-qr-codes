from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.views.generic.edit import FormView
from users import forms

import logging
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .forms import AddressForm
from .models import Address, User
#from django.contrib.admin.views.decorators import staff_member_required # Only staff member has access

logger = logging.getLogger(__name__)


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = forms.UserCreationForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('restaurants-index'))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()  # save user
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "Nowa rejestracja dla adresu email={} przy użyciu RegistrationView", email
        )

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


class AddressListView(LoginRequiredMixin, ListView):
    '''

    '''
    model = Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'users/address_form.html'

    form_class = AddressForm

    success_url = reverse_lazy("users-address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = [
        "address2",
        "house_number",
        "flat_number",
    ]
    success_url = reverse_lazy("users-address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy("users-address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)