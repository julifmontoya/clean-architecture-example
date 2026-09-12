import django.db.models.deletion
from django.db import migrations, models


def migrate_rates_to_tour(apps, schema_editor):
    TourAvailability = apps.get_model("inventory", "TourAvailability")
    TourRate = apps.get_model("inventory", "TourRate")

    tour_ids = set(TourAvailability.objects.values_list("tour_id", flat=True))

    for tour_id in tour_ids:
        rates = TourRate.objects.filter(availability__tour_id=tour_id).order_by("price_adult")
        chosen = rates.first()
        if chosen is None:
            continue

        TourRate.objects.filter(availability__tour_id=tour_id).exclude(pk=chosen.pk).delete()

        chosen.tour_id = tour_id
        chosen.save(update_fields=["tour_id"])

    TourRate.objects.filter(tour_id__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_tour_duration"),
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourrate",
            name="tour",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rate",
                to="catalog.tour",
            ),
        ),
        migrations.RunPython(migrate_rates_to_tour, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="tourrate",
            name="availability",
        ),
        migrations.AlterField(
            model_name="tourrate",
            name="tour",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rate",
                to="catalog.tour",
            ),
        ),
        migrations.DeleteModel(
            name="TourAvailability",
        ),
    ]
