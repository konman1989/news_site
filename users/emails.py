from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from django.shortcuts import reverse

from news.celery import app
from .models import CustomUser
from .tokens import account_activation_token


@app.task
def send_account_confirmation_email(user_id, current_site):
    user = CustomUser.objects.get(pk=user_id)
    token = account_activation_token.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"{current_site}{reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})}"
    message = get_template('users/register_email.html').render({
        'confirm_url': activation_link
    })

    mail = EmailMessage('Confirm your account', message,
                        to=[user.email],
                        from_email=settings.EMAIL_HOST_UER)
    mail.content_subtype = 'html'
    mail.send()