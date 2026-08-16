from rest_framework import serializers

from modules.inventory.models import TourAvailability
from modules.inventory.presentation.serializers.rate_serializer import TourRateSerializer


class TourAvailabilitySerializer(serializers.ModelSerializer):
    rate = TourRateSerializer()

    class Meta:
        model = TourAvailability
        fields = ["id", "date", "allotment", "rate"]
        read_only_fields = ["id"]
