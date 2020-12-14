from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm as UsrCreationForm, PasswordResetForm
from django.contrib.auth.forms import UsernameField

from .models import Address, User

from . import models


class UserCreationForm(UsrCreationForm):
    class Meta(UsrCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

    def send_mail(self):
        message = f'Witaj, {self.cleaned_data["email"]}!\n' \
                  'Dziękujemy za założenie konta na Studentzamawia.pl' \
                  '\n \n' \
                  'Wiadomość wygenerowana automatycznie (proszę na nią nie odpowiadać).'
        send_mail(
            'Witamy!',
            message,
            'administracja@studentzamawia.pl',
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


class ValidateEmailForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Użytkownik o podanym adresie e-mail nie jest zarejestrowany")
        return email

