import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_api.settings")

import django

django.setup()

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="test@example.com", password="password"
    )
    assert user.email == "test@example.com"
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.check_password("password") is True


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(
        email="admin@example.com", password="admin"
    )
    assert superuser.email == "admin@example.com"
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.check_password("admin") is True
