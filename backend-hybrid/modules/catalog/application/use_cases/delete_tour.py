from modules.catalog.models import Tour


class DeleteTour:
    def execute(self, tour_id: int) -> None:
        Tour.objects.filter(id=tour_id).delete()