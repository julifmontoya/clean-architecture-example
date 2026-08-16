from django.db.models import Min

from modules.catalog.models import Tour


class GetTour:
    def execute(self, tour_id: int) -> Tour:
        tour = (
            Tour.objects.select_related("category")
            .annotate(min_price_adult=Min("availabilities__rate__price_adult"))
            .filter(id=tour_id)
            .first()
        )
        if tour is None:
            raise ValueError(f"Tour {tour_id} does not exist.")
        return tour