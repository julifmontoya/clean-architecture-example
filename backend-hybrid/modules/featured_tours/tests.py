from rest_framework.test import APITestCase

from modules.catalog.models import Category, Tour
from modules.inventory.models import TourRate


class FeaturedToursAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Adventure")

    def _create_tour(self, title, **overrides):
        defaults = dict(
            title=title,
            description="A tour.",
            duration=1,
            itinerary_days=[{"day": 1, "description": "Day trip"}],
            included_not_included={"included": [], "not_included": []},
            category=self.category,
        )
        defaults.update(overrides)
        return Tour.objects.create(**defaults)

    def _add_rate(self, tour, price_adult):
        TourRate.objects.create(
            tour=tour,
            price_adult=price_adult,
            price_child=price_adult,
            price_infant=price_adult,
        )

    def test_returns_featured_tours_with_price(self):
        tour = self._create_tour("Cartagena y Islas del Rosario", duration=3)
        self._add_rate(tour, "100")

        response = self.client.get("/v1/featured-tours/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Cartagena y Islas del Rosario")
        self.assertEqual(response.data[0]["min_price_adult"], "100.00")
        self.assertIn("category", response.data[0])
        self.assertIn("description", response.data[0])
        self.assertIn("duration", response.data[0])

    def test_tour_without_price_returns_null_price(self):
        self._create_tour("Excursión de un Día a Barú", duration=1)

        response = self.client.get("/v1/featured-tours/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data[0]["min_price_adult"])

    def test_limits_results_to_default_count(self):
        for i in range(5):
            self._create_tour(f"Tour {i}")

        response = self.client.get("/v1/featured-tours/")

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data), 3)
