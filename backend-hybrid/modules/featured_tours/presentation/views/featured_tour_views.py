from rest_framework import generics

from modules.featured_tours.application.use_cases.list_featured_tours import ListFeaturedTours
from modules.featured_tours.presentation.serializers.featured_tour_serializer import (
    FeaturedTourSerializer,
)


class FeaturedTourListAPIView(generics.ListAPIView):
    serializer_class = FeaturedTourSerializer

    def get_queryset(self):
        return ListFeaturedTours().execute()
