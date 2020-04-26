import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=DateInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'date_of_birth']

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']
        if date is not None:
            if date > datetime.date.today():
                raise ValidationError('Birthday date should be in the past.')
        return date


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login':
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive.",
        'inactive':
            "This account is inactive. Please confirm your account first.",
    }
