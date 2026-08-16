from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title or not self.title.strip():
            raise ValueError("Category must have a title.")
        super().save(*args, **kwargs)


class Tour(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    duration = models.IntegerField(default=0)
    itinerary_days = models.JSONField()
    included_not_included = models.JSONField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tours")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title or not self.title.strip():
            raise ValueError("Tour must have a title.")
        super().save(*args, **kwargs)
