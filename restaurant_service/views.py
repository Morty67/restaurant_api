from datetime import date

from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response

from restaurant_service.models import Restaurant, Menu, Vote
from restaurant_service.permissions import IsAdminOrReadOnly
from restaurant_service.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializer,
    TopMenuSerializer,
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
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        menu_id = request.data.get("menu")

        # Check if the menu with the specified identifier exists and corresponds to today's date.
        try:
            menu = Menu.objects.get(id=menu_id, date=date.today())
        except Menu.DoesNotExist:
            return Response(
                {
                    "error": "Invalid menu ID or menu is not available for voting"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the employee has already voted for this menu.
        if Vote.objects.filter(worker=request.user, menu=menu).exists():
            return Response(
                {"error": "You have already voted for this menu"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new vote.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Increase the vote counter in the menu.
        menu.vote_count += 1
        menu.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TopMenuView(generics.ListAPIView):
    serializer_class = TopMenuSerializer

    def get_queryset(self):
        today = date.today()
        top_menus = Menu.objects.filter(date=today).order_by("-vote_count")[:3]
        return top_menus
