from django.contrib import admin

from .models import TourRate


@admin.register(TourRate)
class TourRateAdmin(admin.ModelAdmin):
    list_display = ("id", "tour", "price_adult", "price_child", "price_infant")
    search_fields = ("tour__title",)
