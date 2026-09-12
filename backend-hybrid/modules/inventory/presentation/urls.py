from django.urls import path

from modules.inventory.presentation.views.rate_views import TourRateAPIView

urlpatterns = [
    path(
        "tours/<int:tour_id>/rate/",
        TourRateAPIView.as_view(),
        name="tour-rate-detail",
    ),
]
