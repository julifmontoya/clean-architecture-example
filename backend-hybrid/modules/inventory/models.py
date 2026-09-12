from django.db import models

from modules.catalog.models import Tour


class TourRate(models.Model):
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE, related_name="rate")
    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2)
    price_infant = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rate for {self.tour}"
