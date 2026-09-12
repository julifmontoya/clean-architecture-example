from django.db.models import QuerySet

from modules.catalog.application.use_cases.list_tours import ListTours
from modules.catalog.models import Tour

DEFAULT_FEATURED_TOURS_LIMIT = 3


class ListFeaturedTours:
    def execute(self, limit: int = DEFAULT_FEATURED_TOURS_LIMIT) -> QuerySet[Tour]:
        return ListTours().execute().order_by("id")[:limit]
