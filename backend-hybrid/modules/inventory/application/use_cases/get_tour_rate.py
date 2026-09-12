from modules.inventory.models import TourRate


class GetTourRate:
    def execute(self, tour_id: int) -> TourRate | None:
        return TourRate.objects.filter(tour_id=tour_id).first()
