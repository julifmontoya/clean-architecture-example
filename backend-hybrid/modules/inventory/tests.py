from rest_framework.test import APITestCase

from modules.catalog.models import Category, Tour
from modules.inventory.models import TourAvailability, TourRate


class TourAvailabilityTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(title="Adventure")
        self.tour = Tour.objects.create(
            title="Cartagena Tour",
            description="A tour through Cartagena.",
            itinerary_days=[{"day": 1, "description": "City tour"}],
            included_not_included={"included": ["Guide"], "not_included": ["Flights"]},
            category=category,
        )

    def _payload(self, date, allotment, price_adult, price_child, price_infant):
        return {
            "date": date,
            "allotment": allotment,
            "rate": {
                "price_adult": price_adult,
                "price_child": price_child,
                "price_infant": price_infant,
            },
        }

    def test_create_multiple_availabilities_each_with_its_own_rate(self):
        response_1 = self.client.post(
            f"/v1/tours/{self.tour.id}/availabilities/",
            self._payload("2026-08-20", 10, "100000", "80000", "20000"),
            format="json",
        )
        response_2 = self.client.post(
            f"/v1/tours/{self.tour.id}/availabilities/",
            self._payload("2026-08-21", 8, "110000", "85000", "20000"),
            format="json",
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)

        self.assertEqual(self.tour.availabilities.count(), 2)
        self.assertEqual(TourRate.objects.count(), 2)

        first = TourAvailability.objects.get(date="2026-08-20")
        self.assertEqual(first.allotment, 10)
        self.assertEqual(str(first.rate.price_adult), "100000.00")
        self.assertEqual(str(first.rate.price_child), "80000.00")
        self.assertEqual(str(first.rate.price_infant), "20000.00")

    def test_list_availabilities_includes_rate(self):
        self.client.post(
            f"/v1/tours/{self.tour.id}/availabilities/",
            self._payload("2026-08-20", 10, "100000", "80000", "20000"),
            format="json",
        )

        response = self.client.get(f"/v1/tours/{self.tour.id}/availabilities/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["allotment"], 10)
        self.assertEqual(response.data[0]["rate"]["price_adult"], "100000.00")

    def test_create_availability_requires_existing_tour(self):
        response = self.client.post(
            "/v1/tours/999999/availabilities/",
            self._payload("2026-08-20", 10, "100000", "80000", "20000"),
            format="json",
        )

        self.assertEqual(response.status_code, 400)
