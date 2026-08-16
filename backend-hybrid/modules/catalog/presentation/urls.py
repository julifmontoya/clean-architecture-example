from django.urls import path

from modules.catalog.presentation.views.category_views import CategoryListCreateAPIView
from modules.catalog.presentation.views.tour_views import TourDetailAPIView, TourListCreateAPIView

urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("tours/", TourListCreateAPIView.as_view(), name="tour-list-create"),
    path("tours/<int:tour_id>/", TourDetailAPIView.as_view(), name="tour-detail"),
]