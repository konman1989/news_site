import pytest
from django.urls import reverse

from users.models import CustomUser


@pytest.mark.django_db
def test_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user
    url = reverse('login')
    response = client.get(url)
    assert response.context['user'].is_authenticated


@pytest.mark.django_db
def test_registration_view_post_success(create_db, client, test_password):
    url = reverse('register')
    client.post(url,
                data={'email': 'test@test.com',
                      'password1': test_password,
                      'password2': test_password}
                )

    assert CustomUser.objects.count() == 4


