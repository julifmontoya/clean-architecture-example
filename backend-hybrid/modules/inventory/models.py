from django.db import models

from modules.catalog.models import Tour


class TourAvailability(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="availabilities")
    date = models.DateField()
    allotment = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.tour.title} - {self.date}"


class TourRate(models.Model):
    availability = models.OneToOneField(TourAvailability, on_delete=models.CASCADE, related_name="rate")
    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2)
    price_infant = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rate for {self.availability}"
