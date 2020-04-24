from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'manoilo.blog@gmail.com',
    ['asu.cart@gmail.com'],
    html_message='<h1>Hey there</h1>',
    fail_silently=False,
)

