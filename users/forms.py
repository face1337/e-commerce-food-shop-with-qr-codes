from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm as UsrCreationForm
from django.contrib.auth.forms import UsernameField

from .models import Address

from . import models


class UserCreationForm(UsrCreationForm):
    class Meta(UsrCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

    def send_mail(self):
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



