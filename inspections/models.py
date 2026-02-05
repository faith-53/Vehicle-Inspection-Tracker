from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Inspection(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_PASSED = "passed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_PASSED, "Passed"),
        (STATUS_FAILED, "Failed"),
    ]

    vehicle_plate = models.CharField(max_length=20)
    inspection_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    notes = models.TextField(blank=True)

    def clean(self):
        super().clean()
        today = timezone.localdate()
        if self.inspection_date < today:
            raise ValidationError({"inspection_date": "Inspection date cannot be in the past."})

        valid_statuses = {choice[0] for choice in self.STATUS_CHOICES}
        if self.status not in valid_statuses:
            raise ValidationError({"status": "Status must be one of: scheduled, passed, failed."})

    def __str__(self):
        return f"{self.vehicle_plate} on {self.inspection_date} ({self.status})"
