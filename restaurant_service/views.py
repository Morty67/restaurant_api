from datetime import date

from rest_framework import viewsets, status, generics, permissions, versioning
from rest_framework.response import Response

from restaurant_service.models import Restaurant, Menu, Vote
from restaurant_service.permissions import IsAdminOrReadOnly
from restaurant_service.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    TopMenuSerializer,
    VoteSerializerV2,
    VoteSerializerV1,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]

    def create(self, request, *args, **kwargs):
        # Retrieve data from the request.
        restaurant_id = request.data.get("restaurant")
        date = request.data.get("date")
        menu_file = request.data.get("menu_file")

        # Check if a restaurant with the specified identifier exists.
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Invalid restaurant ID"}, status=400)

        # Create a new menu object.
        menu = Menu(restaurant=restaurant, date=date, menu_file=menu_file)
        menu.save()

        # Return the created menu object in the response.
        serializer = self.get_serializer(menu)
        return Response(serializer.data, status=201)


class TodayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = date.today()
        return Menu.objects.filter(date=today)


class VoteView(generics.CreateAPIView):
    versioning_class = versioning.AcceptHeaderVersioning
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        version = self.request.version
        if version == "1.0":
            return VoteSerializerV1
        elif version == "2.0":
            return VoteSerializerV2

        return VoteSerializerV2

    def get_queryset(self):
        # Return an empty queryset since it is not used for database
        # operations.
        return Vote.objects.none()

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TopMenuView(generics.ListAPIView):
    serializer_class = TopMenuSerializer
    versioning_class = versioning.AcceptHeaderVersioning

    def get_queryset(self):
        today = date.today()
        queryset = Menu.objects.filter(date=today)
        if self.request.version == "1.0":
            queryset = queryset.order_by("-vote_count")[:1]
        elif self.request.version == "2.0":
            queryset = queryset.order_by("-vote_count")[:3]
        return queryset
