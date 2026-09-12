from rest_framework.test import APITestCase

from modules.catalog.models import Category, Tour
from modules.inventory.models import TourRate


class TourRateTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(title="Adventure")
        self.tour = Tour.objects.create(
            title="Cartagena Tour",
            description="A tour through Cartagena.",
            itinerary_days=[{"day": 1, "description": "City tour"}],
            included_not_included={"included": ["Guide"], "not_included": ["Flights"]},
            category=category,
        )

    def _payload(self, price_adult, price_child, price_infant):
        return {
            "price_adult": price_adult,
            "price_child": price_child,
            "price_infant": price_infant,
        }

    def test_set_rate_creates_it(self):
        response = self.client.put(
            f"/v1/tours/{self.tour.id}/rate/",
            self._payload("100000", "80000", "20000"),
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["price_adult"], "100000.00")
        self.assertEqual(response.data["price_child"], "80000.00")
        self.assertEqual(response.data["price_infant"], "20000.00")

        self.assertEqual(TourRate.objects.count(), 1)
        rate = TourRate.objects.get(tour=self.tour)
        self.assertEqual(str(rate.price_adult), "100000.00")

    def test_set_rate_updates_existing_rate_instead_of_duplicating(self):
        self.client.put(
            f"/v1/tours/{self.tour.id}/rate/",
            self._payload("100000", "80000", "20000"),
            format="json",
        )

        response = self.client.put(
            f"/v1/tours/{self.tour.id}/rate/",
            self._payload("110000", "85000", "25000"),
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TourRate.objects.count(), 1)
        rate = TourRate.objects.get(tour=self.tour)
        self.assertEqual(str(rate.price_adult), "110000.00")

    def test_get_rate_returns_the_current_rate(self):
        self.client.put(
            f"/v1/tours/{self.tour.id}/rate/",
            self._payload("100000", "80000", "20000"),
            format="json",
        )

        response = self.client.get(f"/v1/tours/{self.tour.id}/rate/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["price_adult"], "100000.00")

    def test_get_rate_returns_404_when_tour_has_no_rate(self):
        response = self.client.get(f"/v1/tours/{self.tour.id}/rate/")

        self.assertEqual(response.status_code, 404)

    def test_set_rate_requires_existing_tour(self):
        response = self.client.put(
            "/v1/tours/999999/rate/",
            self._payload("100000", "80000", "20000"),
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_tour_detail_includes_prices_from_rate(self):
        TourRate.objects.create(
            tour=self.tour,
            price_adult="100000",
            price_child="80000",
            price_infant="20000",
        )

        response = self.client.get(f"/v1/tours/{self.tour.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["min_price_adult"], "100000.00")
        self.assertEqual(response.data["price_child"], "80000.00")
        self.assertEqual(response.data["price_infant"], "20000.00")

    def test_tour_detail_without_rate_has_null_prices(self):
        response = self.client.get(f"/v1/tours/{self.tour.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data["min_price_adult"])
        self.assertIsNone(response.data["price_child"])
        self.assertIsNone(response.data["price_infant"])
