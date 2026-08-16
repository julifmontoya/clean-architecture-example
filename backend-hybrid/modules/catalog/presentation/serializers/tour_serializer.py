from rest_framework import serializers

from modules.catalog.models import Tour
from modules.catalog.presentation.serializers.category_serializer import CategorySerializer


class TourSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    min_price_adult = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, allow_null=True
    )

    class Meta:
        model = Tour
        fields = [
            "id",
            "title",
            "description",
            "duration",
            "itinerary_days",
            "included_not_included",
            "category",
            "category_id",
            "min_price_adult",
        ]
        read_only_fields = ["id"]