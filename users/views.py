from django.views.generic.edit import FormView
from users import forms

from .models import Profile, User

import logging
from django.contrib.auth import login,authenticate
from django.contrib import messages

logger = logging.getLogger(__name__)


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
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

