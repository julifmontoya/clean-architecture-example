from django.db.models import F, QuerySet

from modules.catalog.models import Tour


class ListTours:
    def execute(self) -> QuerySet[Tour]:
        return (
            Tour.objects.select_related("category", "rate")
            .annotate(
                min_price_adult=F("rate__price_adult"),
                price_child=F("rate__price_child"),
                price_infant=F("rate__price_infant"),
            )
        )
