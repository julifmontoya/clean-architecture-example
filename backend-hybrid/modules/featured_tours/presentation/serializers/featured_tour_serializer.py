from rest_framework import serializers

from modules.catalog.models import Tour
from modules.catalog.presentation.serializers.category_serializer import CategorySerializer


class FeaturedTourSerializer(serializers.ModelSerializer):
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
            "category",
            "min_price_adult",
        ]
        read_only_fields = fields
