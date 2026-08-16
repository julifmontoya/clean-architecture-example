from django.urls import path

from modules.inventory.presentation.views.availability_views import TourAvailabilityListCreateAPIView

urlpatterns = [
    path(
        "tours/<int:tour_id>/availabilities/",
        TourAvailabilityListCreateAPIView.as_view(),
        name="tour-availability-list-create",
    ),
]
