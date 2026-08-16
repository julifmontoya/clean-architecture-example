from django.contrib import admin

from .models import TourAvailability, TourRate


@admin.register(TourAvailability)
class TourAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "tour", "date", "allotment")
    list_filter = ("tour",)
    search_fields = ("tour__title",)


@admin.register(TourRate)
class TourRateAdmin(admin.ModelAdmin):
    list_display = ("id", "availability", "price_adult", "price_child", "price_infant")
