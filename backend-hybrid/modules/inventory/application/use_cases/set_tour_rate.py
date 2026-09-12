from modules.catalog.models import Tour
from modules.inventory.models import TourRate


class SetTourRate:
    def execute(
        self,
        tour_id: int,
        price_adult,
        price_child,
        price_infant,
    ) -> TourRate:
        tour = Tour.objects.filter(id=tour_id).first()
        if tour is None:
            raise ValueError(f"Tour {tour_id} does not exist.")

        rate, _ = TourRate.objects.update_or_create(
            tour=tour,
            defaults={
                "price_adult": price_adult,
                "price_child": price_child,
                "price_infant": price_infant,
            },
        )
        return rate
