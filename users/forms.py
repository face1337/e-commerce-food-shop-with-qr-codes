from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm as UsrCreationForm
from django.contrib.auth.forms import UsernameField

import logging

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
