from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template


def send_new_comment_email(comment, receiver):
    message = get_template('blog/comment_email.html').render(comment)

    mail = EmailMessage('You have a new comment to your post', message,
                        to=[receiver],
                        from_email=settings.EMAIL_HOST_UER)
    mail.content_subtype = 'html'
    mail.send()