from django.db.models import Min, QuerySet

from modules.catalog.models import Tour


class ListTours:
    def execute(self) -> QuerySet[Tour]:
        return (
            Tour.objects.select_related("category")
            .annotate(min_price_adult=Min("availabilities__rate__price_adult"))
        )