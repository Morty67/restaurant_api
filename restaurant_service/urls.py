from django.urls import path, include
from rest_framework import routers

from restaurant_service.views import (
    RestaurantViewSet,
    MenuViewSet,
    VoteView,
    TodayMenuView,
    TopMenuView,
)

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet,  basename="restaurants")
router.register("menus", MenuViewSet,   basename="menus")


urlpatterns = [
    path("", include(router.urls)),
    path("votes/", VoteView.as_view(), name="create-vote"),
    path("today/", TodayMenuView.as_view(), name="today-menu"),
    path("result/", TopMenuView.as_view(), name="result-votes"),



]

app_name = "restaurant"
