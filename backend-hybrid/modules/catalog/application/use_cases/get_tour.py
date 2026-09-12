from django.db.models import F

from modules.catalog.models import Tour


class GetTour:
    def execute(self, tour_id: int) -> Tour:
        tour = (
            Tour.objects.select_related("category", "rate")
            .annotate(
                min_price_adult=F("rate__price_adult"),
                price_child=F("rate__price_child"),
                price_infant=F("rate__price_infant"),
            )
            .filter(id=tour_id)
            .first()
        )
        if tour is None:
            raise ValueError(f"Tour {tour_id} does not exist.")
        return tour
