from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.inventory.application.use_cases.get_tour_rate import GetTourRate
from modules.inventory.application.use_cases.set_tour_rate import SetTourRate
from modules.inventory.presentation.serializers.rate_serializer import TourRateSerializer


class TourRateAPIView(APIView):
    def get(self, request, tour_id):
        rate = GetTourRate().execute(tour_id)
        if rate is None:
            raise NotFound(f"Tour {tour_id} does not have a rate yet.")
        return Response(TourRateSerializer(rate).data)

    def put(self, request, tour_id):
        serializer = TourRateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            rate = SetTourRate().execute(
                tour_id=tour_id,
                price_adult=data["price_adult"],
                price_child=data["price_child"],
                price_infant=data["price_infant"],
            )
        except ValueError as error:
            raise ValidationError(str(error))

        return Response(TourRateSerializer(rate).data)
