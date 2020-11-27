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
        redirect_to = self.request.GET.get("")