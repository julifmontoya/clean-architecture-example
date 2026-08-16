from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from modules.catalog.application.use_cases.create_tour import CreateTour
from modules.catalog.application.use_cases.delete_tour import DeleteTour
from modules.catalog.application.use_cases.get_tour import GetTour
from modules.catalog.application.use_cases.list_tours import ListTours
from modules.catalog.application.use_cases.update_tour import UpdateTour
from modules.catalog.presentation.serializers.tour_serializer import TourSerializer
from modules.catalog.presentation.filters.tour_filter import TourFilter


from django_filters.rest_framework import DjangoFilterBackend


class TourListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourFilter

    def get_queryset(self):
        return ListTours().execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            tour = CreateTour().execute(
                title=data["title"],
                description=data.get("description", ""),
                duration=data.get("duration", 0),
                itinerary_days=data["itinerary_days"],
                included_not_included=data["included_not_included"],
                category_id=data["category_id"],
            )
        except ValueError as error:
            raise ValidationError(str(error))

        return Response(
            self.get_serializer(tour).data,
            status=201,
        )


class TourDetailAPIView(APIView):
    def get(self, request, tour_id):
        try:
            tour = GetTour().execute(tour_id)
        except ValueError as error:
            raise NotFound(str(error))
        return Response(TourSerializer(tour).data)

    def put(self, request, tour_id):
        serializer = TourSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            tour = UpdateTour().execute(
                tour_id=tour_id,
                title=data["title"],
                description=data.get("description", ""),
                duration=data.get("duration", 0),
                itinerary_days=data["itinerary_days"],
                included_not_included=data["included_not_included"],
                category_id=data["category_id"],
            )
        except ValueError as error:
            raise NotFound(str(error))

        return Response(TourSerializer(tour).data)

    def delete(self, request, tour_id):
        DeleteTour().execute(tour_id)
        return Response(status=204)