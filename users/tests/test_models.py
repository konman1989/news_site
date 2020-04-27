import pytest
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group, Permission

from users.models import CustomUser


@pytest.mark.django_db
def test_check_user_creation(test_password):
    user = CustomUser.objects.create_user(email='test@test.com',
                                          password=test_password,
                                          first_name='test',
                                          last_name='test',
                                          date_of_birth='1990-01-01')
    assert user.email == 'test@test.com'
    assert check_password(test_password, user.password)
    assert user.first_name == 'test'
    assert user.last_name == 'test'
    assert user.date_of_birth == '1990-01-01'
    assert user.is_active


@pytest.mark.django_db
def test_check_create_superuser(test_password):
    user = CustomUser.objects.create_superuser(email='test@test.com',
                                               password=test_password)
    assert user.is_active
    assert user.is_superuser
    assert user.is_staff


@pytest.mark.django_db
def test_check_user_permissions(create_db):
    user = CustomUser.objects.get(email='user@user.com')
    assert user.email == 'user@user.com'
    assert user.groups.get(name='Users').name == 'Users'
    assert user.has_perm('blog.no_moderation') is False


@pytest.mark.django_db
def test_check_editor_permissions(create_db):
    user = CustomUser.objects.get(email='editor@editor.com')
    assert user.email == 'editor@editor.com'
    assert user.groups.get(name='Editors').name == 'Editors'
    assert user.has_perm('blog.no_moderation')


@pytest.mark.django_db
def test_change_group_permission(create_db):
    group = Group.objects.get(name='Users')
    permission = Permission.objects.get(codename='no_moderation')
    group.permissions.add(permission)
    user = CustomUser.objects.get(email='user@user.com')
    assert user.has_perm('blog.no_moderation')