from rest_framework import serializers

from modules.inventory.models import TourRate


class TourRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRate
        fields = ["price_adult", "price_child", "price_infant"]
