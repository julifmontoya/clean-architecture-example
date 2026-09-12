from django.urls import path

from modules.featured_tours.presentation.views.featured_tour_views import FeaturedTourListAPIView

urlpatterns = [
    path("featured-tours/", FeaturedTourListAPIView.as_view(), name="featured-tour-list"),
]
