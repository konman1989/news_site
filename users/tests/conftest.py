import pytest
from django.core.management import call_command
from django.contrib.auth.models import Group

from users.models import CustomUser
from blog.models import Post


@pytest.fixture
def create_db(db):
    call_command('loaddata', 'users.json', 'groups.json')


@pytest.fixture
def test_password():
    yield 'testing12345'


@pytest.fixture
def create_user(test_password):
    user = CustomUser.objects.create_user(email='test@test.com',
                                          password=test_password,
                                          first_name='test',
                                          last_name='test',
                                          date_of_birth='1990-01-01')
    yield user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    user = create_user
    client.login(email=user.email, password=test_password)
    yield client, user


@pytest.fixture
def create_post():
    def _create_post(author, title='Test Title', content='Test Content'):
        return Post.objects.create(title=title, content=content, author=author)
    yield _create_post


@pytest.fixture
def editors_group(create_db):
    yield Group.objects.get(name='Editors')