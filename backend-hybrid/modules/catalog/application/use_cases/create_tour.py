from modules.catalog.models import Category, Tour


class CreateTour:
    def execute(
        self,
        title: str,
        description: str,
        duration: int,
        itinerary_days: dict,
        included_not_included: dict,
        category_id: int,
    ) -> Tour:
        category = Category.objects.filter(id=category_id).first()
        if category is None:
            raise ValueError(f"Category {category_id} does not exist.")

        tour = Tour(
            title=title,
            description=description,
            duration=duration,
            itinerary_days=itinerary_days,
            included_not_included=included_not_included,
            category=category,
        )
        tour.save()
        return tour
