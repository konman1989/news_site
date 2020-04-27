import pytest


@pytest.mark.django_db
def test_post_not_published_created_by_regular_user(create_user, create_post):
    user = create_user
    post = create_post(author=user)
    post.approve_post()  # post is not approved
    assert post.status == 0


@pytest.mark.django_db
def test_post_published_created_by_editor(create_user, editors_group, create_post):
    user = create_user
    user.groups.add(editors_group)
    user.groups.add(editors_group)
    post = create_post(author=user)
    post.approve_post()  # post is approved
    assert post.status == 1


@pytest.mark.django_db
def test_post_published_created_by_admin(create_user, editors_group,
                                         create_post):
    user = create_user
    user.groups.add(editors_group)
    post = create_post(author=user)
    post.approve_post()  # post is approved
    assert post.status == 1



