import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_api.settings")

import django

django.setup()

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from restaurant_service.models import Restaurant
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "adm@adm.com",
        "password": "password",
        "is_staff": True,
    }


@pytest.fixture
def create_user(user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def restaurant_data():
    return {
        "name": "Test Restaurant",
        "address": "Test Address",
        "contact_info": "Test Contact Info",
    }


@pytest.fixture
def create_restaurant(restaurant_data):
    return Restaurant.objects.create(**restaurant_data)


@patch("restaurant_service.views.RestaurantViewSet.permission_classes", [])
def test_list_restaurants():
    client = APIClient()
    url = reverse("restaurant:restaurants-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


def test_create_restaurant_without_authentication(restaurant_data):
    client = APIClient()
    url = reverse("restaurant:restaurants-list")
    response = client.post(url, data=restaurant_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_restaurant_as_admin(create_user, restaurant_data):
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("restaurant:restaurants-list")
    response = client.post(url, data=restaurant_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == restaurant_data["name"]


def test_create_menu_as_admin(create_user, create_restaurant):
    client = APIClient()
    client.force_authenticate(user=create_user)

    menu_data = {
        "restaurant": create_restaurant.id,
        "date": "2023-06-30",
        "menu_file": "path/to/menu.pdf",
    }

    url = reverse("restaurant:menus-list")
    response = client.post(url, data=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["restaurant"] == create_restaurant.id
    assert response.data["date"] == menu_data["date"]


@pytest.mark.django_db
def test_get_top_menu_version_1():
    client = APIClient()
    url = reverse("restaurant:result-votes")
    headers = {"Accept": "application/json; version=1.0"}
    response = client.get(url, format="json", headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_top_menu_version_2():
    client = APIClient()
    url = reverse("restaurant:result-votes")
    headers = {"Accept": "application/json; version=2.0"}
    response = client.get(url, format="json", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_list_menus():
    client = APIClient()
    url = reverse("restaurant:menus-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


def test_get_today_menu():
    client = APIClient()

    # Authenticate as admin
    admin_user = User.objects.create_superuser(
        email="admin@example.com", password="admin"
    )
    client.force_authenticate(user=admin_user)

    url = reverse("restaurant:today-menu")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_top_menu_version_1():
    client = APIClient()
    url = reverse("restaurant:result-votes")
    headers = {"Accept": "application/json; version=1.0"}
    response = client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK


def test_top_menu_version_2():
    client = APIClient()
    url = reverse("restaurant:result-votes")
    headers = {"Accept": "application/json; version=2.0"}
    response = client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK
