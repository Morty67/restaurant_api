from datetime import date

from rest_framework import serializers

from restaurant_service.models import Restaurant, Menu, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name", read_only=True
    )
    vote_count = serializers.ReadOnlyField()

    class Meta:
        model = Menu
        fields = [
            "id",
            "date",
            "menu_file",
            "restaurant",
            "restaurant_name",
            "vote_count",
        ]


class VoteSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(date=date.today())
    )

    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ("worker",)

    def create(self, validated_data):
        menu = validated_data.get("menu")
        menu.vote_count += 1
        menu.save()

        validated_data["worker"] = self.context["request"].user
        return super().create(validated_data)


class TopMenuSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name")
    vote_count = serializers.SerializerMethodField()

    def get_vote_count(self, obj):
        return obj.vote_count

    class Meta:
        model = Menu
        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "date",
            "menu_file",
            "vote_count",
        ]
