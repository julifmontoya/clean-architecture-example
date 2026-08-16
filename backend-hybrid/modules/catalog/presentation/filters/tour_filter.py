import django_filters

from modules.catalog.models import Tour


class TourFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Tour
        fields = ["category", "duration", "title"]
