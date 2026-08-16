from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.inventory.application.use_cases.create_availability import CreateAvailability
from modules.inventory.application.use_cases.list_availabilities import ListAvailabilities
from modules.inventory.presentation.serializers.availability_serializer import TourAvailabilitySerializer


class TourAvailabilityListCreateAPIView(APIView):
    def get(self, request, tour_id):
        availabilities = ListAvailabilities().execute(tour_id)
        return Response(TourAvailabilitySerializer(availabilities, many=True).data)

    def post(self, request, tour_id):
        serializer = TourAvailabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        rate = data["rate"]

        try:
            availability = CreateAvailability().execute(
                tour_id=tour_id,
                date=data["date"],
                allotment=data.get("allotment", 0),
                price_adult=rate["price_adult"],
                price_child=rate["price_child"],
                price_infant=rate["price_infant"],
            )
        except ValueError as error:
            raise ValidationError(str(error))

        return Response(TourAvailabilitySerializer(availability).data, status=201)
