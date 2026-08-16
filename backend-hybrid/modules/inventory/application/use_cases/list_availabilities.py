from modules.inventory.models import TourAvailability


class ListAvailabilities:
    def execute(self, tour_id: int) -> list[TourAvailability]:
        return list(
            TourAvailability.objects.select_related("rate").filter(tour_id=tour_id)
        )
