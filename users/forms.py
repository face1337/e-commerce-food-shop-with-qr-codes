from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm as UsrCreationForm
from django.contrib.auth.forms import UsernameField

import logging

from .models import Address
from orders.models import Order

logger = logging.getLogger(__name__)

from . import models


class UserCreationForm(UsrCreationForm):
    class Meta(UsrCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

    def send_mail(self):
        logger.info(
            "Wysyłanie rejestracyjnej wiadomości email do {}".format(self.cleaned_data["email"])
        )
        message = "Witaj{}".format(format(self.cleaned_data["email"]))
        send_mail(
            "Witamy!",
            message,
            "administracja@studentzamawia.domain",
            [self.cleaned_data["email"]],
            fail_silently=True,
        )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("address2", "house_number", "flat_number")


class AddressSelectionForm(forms.Form):
    shipping_address = forms.ModelChoiceField(queryset=None, label="Adres dostawy")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Address.objects.filter(user=user)
        self.fields['shipping_address'].queryset = queryset


class CreateAddressForUnregisteredUser(forms.Form):
    class Meta:
        model = Order
        fields = ['shipping_address1']

