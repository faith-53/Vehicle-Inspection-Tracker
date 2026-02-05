from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Inspection


class InspectionApiTests(TestCase):
    def test_successful_inspection_creation_with_valid_data(self):
        """Ensure an inspection is created when data is valid."""
        future_date = (timezone.localdate() + timedelta(days=1)).isoformat()
        payload = {
            "vehicle_plate": "ABC-1234",
            "inspection_date": future_date,
            "status": Inspection.STATUS_SCHEDULED,
            "notes": "Routine check",
        }

        response = self.client.post(
            "/api/inspections",
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Inspection.objects.count(), 1)
        inspection = Inspection.objects.first()
        self.assertEqual(inspection.vehicle_plate, payload["vehicle_plate"])
        self.assertEqual(inspection.status, payload["status"])

    def test_inspection_with_past_date_is_rejected(self):
        """Ensure inspections with past inspection_date are rejected."""
        past_date = (timezone.localdate() - timedelta(days=1)).isoformat()
        payload = {
            "vehicle_plate": "XYZ-9999",
            "inspection_date": past_date,
            "status": Inspection.STATUS_SCHEDULED,
        }

        response = self.client.post(
            "/api/inspections",
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Inspection date cannot be in the past.", response.json().get("error", ""))
        self.assertEqual(Inspection.objects.count(), 0)

