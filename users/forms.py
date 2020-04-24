import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=DateInput, required=False)

    # date check https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Forms
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'date_of_birth']

    def clean_date_of_birth(self):
        # TODO not working
        date = self.cleaned_data['date_of_birth']
        if date > datetime.date.today():
            raise ValidationError('Birthday date should be in past.')
        return date