from rest_framework.test import APITestCase

from modules.catalog.models import Category, Tour


class TourCRUDTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Adventure")
        self.duration = 5
        self.itinerary_days = [
            {"day": 1, "description": "Arrival and city tour"},
            {"day": 2, "description": "Hiking excursion"},
        ]
        self.included_not_included = {
            "included": ["Breakfast", "Transport"],
            "not_included": ["Flights", "Travel insurance"],
        }

    def _payload(self, **overrides):
        payload = {
            "title": "Andes Trek",
            "description": "A trek through the Andes.",
            "duration": self.duration,
            "itinerary_days": self.itinerary_days,
            "included_not_included": self.included_not_included,
            "category_id": self.category.id,
        }
        payload.update(overrides)
        return payload

    def test_create_tour_with_new_fields(self):
        response = self.client.post("/v1/tours/", self._payload(), format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["duration"], self.duration)
        self.assertEqual(response.data["itinerary_days"], self.itinerary_days)
        self.assertEqual(response.data["included_not_included"], self.included_not_included)

        tour = Tour.objects.get(id=response.data["id"])
        self.assertEqual(tour.duration, self.duration)
        self.assertEqual(tour.itinerary_days, self.itinerary_days)
        self.assertEqual(tour.included_not_included, self.included_not_included)

    def test_create_tour_requires_new_fields(self):
        payload = self._payload()
        del payload["itinerary_days"]

        response = self.client.post("/v1/tours/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("itinerary_days", response.data)

    def test_retrieve_tour_includes_new_fields(self):
        tour = Tour.objects.create(
            title="Andes Trek",
            description="A trek through the Andes.",
            duration=self.duration,
            itinerary_days=self.itinerary_days,
            included_not_included=self.included_not_included,
            category=self.category,
        )

        response = self.client.get(f"/v1/tours/{tour.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["duration"], self.duration)
        self.assertEqual(response.data["itinerary_days"], self.itinerary_days)
        self.assertEqual(response.data["included_not_included"], self.included_not_included)

    def test_list_tours_includes_new_fields(self):
        Tour.objects.create(
            title="Andes Trek",
            description="A trek through the Andes.",
            duration=self.duration,
            itinerary_days=self.itinerary_days,
            included_not_included=self.included_not_included,
            category=self.category,
        )

        response = self.client.get("/v1/tours/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["duration"], self.duration)
        self.assertEqual(response.data[0]["itinerary_days"], self.itinerary_days)
        self.assertEqual(response.data[0]["included_not_included"], self.included_not_included)

    def test_update_tour_new_fields(self):
        tour = Tour.objects.create(
            title="Andes Trek",
            description="A trek through the Andes.",
            duration=self.duration,
            itinerary_days=self.itinerary_days,
            included_not_included=self.included_not_included,
            category=self.category,
        )
        new_duration = 8
        new_itinerary_days = [{"day": 1, "description": "Updated plan"}]
        new_included_not_included = {"included": ["Guide"], "not_included": ["Meals"]}

        response = self.client.put(
            f"/v1/tours/{tour.id}/",
            self._payload(
                duration=new_duration,
                itinerary_days=new_itinerary_days,
                included_not_included=new_included_not_included,
            ),
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        tour.refresh_from_db()
        self.assertEqual(tour.duration, new_duration)
        self.assertEqual(tour.itinerary_days, new_itinerary_days)
        self.assertEqual(tour.included_not_included, new_included_not_included)

    def test_create_tour_defaults_duration_when_omitted(self):
        payload = self._payload()
        del payload["duration"]

        response = self.client.post("/v1/tours/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["duration"], 0)
