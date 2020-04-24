from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import CustomUser
from .tokens import account_activation_token
from .forms import RegistrationForm, CustomLoginForm
from .utils import send_account_confirmation_email


class Register(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            send_account_confirmation_email(user, request)
            messages.success(request,
                             'Your account has been created but you need to '
                             'activate it first. You can find the link in '
                             'your email.')

            return render(request, 'users/register_confirmation.html')


class ConfirmRegistrationView(View):

    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))

        user = CustomUser.objects.get(pk=user_id)

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been confirmed. '
                                      'You can login now.')
        return redirect('login')


class Login(LoginView):
    authentication_form = CustomLoginForm


