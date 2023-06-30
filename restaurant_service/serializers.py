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


class VoteSerializerV1(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(date=date.today())
    )

    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["worker"]

    def create(self, validated_data):
        menu = validated_data.get("menu")

        # We are checking if the user has already voted 3 times for this menu.
        user = self.context["request"].user
        if Vote.objects.filter(worker=user, menu=menu).count() >= 3:
            raise serializers.ValidationError(
                "You have reached the maximum number of votes for this menu."
            )

        menu.vote_count += 1
        menu.save()

        validated_data["worker"] = user
        return super().create(validated_data)


class VoteSerializerV2(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(date=date.today())
    )

    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["worker"]

    def create(self, validated_data):
        menu = validated_data.get("menu")

        # We are checking if the user has already voted for this menu.
        user = self.context["request"].user
        if Vote.objects.filter(worker=user, menu=menu).exists():
            raise serializers.ValidationError(
                "You have already voted for this menu."
            )

        menu.vote_count += 1
        menu.save()

        validated_data["worker"] = user
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
