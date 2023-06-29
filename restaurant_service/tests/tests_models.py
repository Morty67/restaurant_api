import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_api.settings")

import django

django.setup()

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from restaurant_service.models import Restaurant, Menu, Vote


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(
        name="Restaurant A", address="Address A", contact_info="Contact A"
    )


@pytest.fixture
def menu(restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=timezone.now().date(),
        menu_file="path/to/menu.pdf",
        vote_count=0,
    )


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        email="testuser@example.com", password="password123"
    )


@pytest.fixture
def vote(menu, user):
    return Vote.objects.create(worker=user, menu=menu)


@pytest.mark.django_db
def test_restaurant_str(restaurant):
    assert str(restaurant) == "Restaurant A"


@pytest.mark.django_db
def test_menu_str(menu):
    expected_str = f"Menu for {timezone.now().date()} - Restaurant A"
    assert str(menu) == expected_str


@pytest.mark.django_db
def test_vote_str(vote):
    expected_str = (
        f"Vote by testuser@example.com for Menu for"
        f" {timezone.now().date()} - Restaurant A"
    )
    assert str(vote) == expected_str
