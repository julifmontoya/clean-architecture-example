from modules.catalog.models import Tour
from modules.inventory.models import TourAvailability, TourRate


class CreateAvailability:
    def execute(
        self,
        tour_id: int,
        date,
        allotment: int,
        price_adult,
        price_child,
        price_infant,
    ) -> TourAvailability:
        tour = Tour.objects.filter(id=tour_id).first()
        if tour is None:
            raise ValueError(f"Tour {tour_id} does not exist.")

        availability = TourAvailability.objects.create(
            tour=tour,
            date=date,
            allotment=allotment,
        )
        TourRate.objects.create(
            availability=availability,
            price_adult=price_adult,
            price_child=price_child,
            price_infant=price_infant,
        )
        return availability
