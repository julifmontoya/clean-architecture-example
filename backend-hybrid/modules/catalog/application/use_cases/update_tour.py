from modules.catalog.models import Category, Tour


class UpdateTour:
    def execute(
        self,
        tour_id: int,
        title: str,
        description: str,
        duration: int,
        itinerary_days: dict,
        included_not_included: dict,
        category_id: int,
    ) -> Tour:
        tour = Tour.objects.filter(id=tour_id).first()
        if tour is None:
            raise ValueError(f"Tour {tour_id} does not exist.")

        category = Category.objects.filter(id=category_id).first()
        if category is None:
            raise ValueError(f"Category {category_id} does not exist.")

        tour.title = title
        tour.description = description
        tour.duration = duration
        tour.itinerary_days = itinerary_days
        tour.included_not_included = included_not_included
        tour.category = category
        tour.save()
        return tour