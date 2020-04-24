from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import CustomUserManager

# class UsersGroup(Group):
#     name = 'users'
#
#     class Meta:
#         abstract = True
#
#
# class EditorsGroup(Group):
#     name = 'editors'
#
#     class Meta:
#         abstract = True


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=32, unique=True)
    date_of_birth = models.DateField(null=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



    # TODO register by email https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
#     https://medium.com/@ramykhuffash/django-authentication-with-just-an-email-and-password-no-username-required-33e47976b517

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

