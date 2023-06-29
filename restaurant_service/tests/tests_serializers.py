import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_api.settings")

import django

django.setup()

import pytest
from datetime import date
from django.contrib.auth import get_user_model
from restaurant_service.models import Restaurant, Menu, Vote
from restaurant_service.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializerV1,
    VoteSerializerV2,
    TopMenuSerializer,
)


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(
        name="Restaurant A", address="Address A", contact_info="Contact A"
    )


@pytest.fixture
def menu(restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=date.today(),
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
def vote(user, menu):
    return Vote.objects.create(worker=user, menu=menu)


@pytest.mark.django_db
def test_restaurant_serializer(restaurant):
    serializer = RestaurantSerializer(instance=restaurant)
    assert serializer.data["name"] == "Restaurant A"


@pytest.mark.django_db
def test_menu_serializer(menu):
    serializer = MenuSerializer(instance=menu)
    assert serializer.data["restaurant_name"] == "Restaurant A"


@pytest.mark.django_db
def test_vote_serializer_v1_create(user, menu):
    request = type("Request", (), {"user": user})()
    serializer = VoteSerializerV1(
        data={"menu": menu.pk}, context={"request": request}
    )
    assert serializer.is_valid()
    serializer.save()
    menu.refresh_from_db()
    assert menu.vote_count == 1


@pytest.mark.django_db
def test_vote_serializer_v2_create(user, menu):
    request = type("Request", (), {"user": user})()
    serializer = VoteSerializerV2(
        data={"menu": menu.pk}, context={"request": request}
    )
    assert serializer.is_valid()
    serializer.save()
    menu.refresh_from_db()
    assert menu.vote_count == 1


@pytest.mark.django_db
def test_top_menu_serializer(menu):
    serializer = TopMenuSerializer(instance=menu)
    assert serializer.data["restaurant_name"] == "Restaurant A"
