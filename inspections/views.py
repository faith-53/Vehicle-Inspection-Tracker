import json
from datetime import datetime

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Inspection


def _parse_request_body(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON body."}, status=400)
    return data, None


@csrf_exempt
def inspections_collection(request):
    if request.method == "GET":
        inspections = Inspection.objects.all().order_by("inspection_date")
        results = [
            {
                "id": insp.id,
                "vehicle_plate": insp.vehicle_plate,
                "inspection_date": insp.inspection_date.isoformat(),
                "status": insp.status,
                "notes": insp.notes,
            }
            for insp in inspections
        ]
        return JsonResponse(results, safe=False)

    if request.method == "POST":
        data, error_response = _parse_request_body(request)
        if error_response:
            return error_response

        required_fields = ["vehicle_plate", "inspection_date", "status"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return JsonResponse(
                {"error": f"Missing required fields: {', '.join(missing)}"},
                status=400,
            )

        vehicle_plate = data.get("vehicle_plate", "").strip()
        inspection_date_raw = data.get("inspection_date")
        status = data.get("status")
        notes = data.get("notes", "").strip()

        try:
            inspection_date = datetime.fromisoformat(inspection_date_raw).date()
        except (TypeError, ValueError):
            return JsonResponse(
                {"error": "inspection_date must be a valid ISO date (YYYY-MM-DD)."},
                status=400,
            )

        today = timezone.localdate()
        if inspection_date < today:
            return JsonResponse(
                {"error": "Inspection date cannot be in the past."},
                status=400,
            )

        valid_statuses = {
            Inspection.STATUS_SCHEDULED,
            Inspection.STATUS_PASSED,
            Inspection.STATUS_FAILED,
        }
        if status not in valid_statuses:
            return JsonResponse(
                {"error": "Status must be one of: scheduled, passed, failed."},
                status=400,
            )

        inspection = Inspection.objects.create(
            vehicle_plate=vehicle_plate,
            inspection_date=inspection_date,
            status=status,
            notes=notes,
        )

        return JsonResponse(
            {
                "id": inspection.id,
                "vehicle_plate": inspection.vehicle_plate,
                "inspection_date": inspection.inspection_date.isoformat(),
                "status": inspection.status,
                "notes": inspection.notes,
            },
            status=201,
        )

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def inspection_detail(request, id):
    inspection = get_object_or_404(Inspection, id=id)

    if request.method == "GET":
        return JsonResponse(
            {
                "id": inspection.id,
                "vehicle_plate": inspection.vehicle_plate,
                "inspection_date": inspection.inspection_date.isoformat(),
                "status": inspection.status,
                "notes": inspection.notes,
            }
        )

    if request.method == "PUT":
        data, error_response = _parse_request_body(request)
        if error_response:
            return error_response

        if "vehicle_plate" in data:
            inspection.vehicle_plate = data["vehicle_plate"].strip()

        if "inspection_date" in data:
            try:
                new_date = datetime.fromisoformat(data["inspection_date"]).date()
            except (TypeError, ValueError):
                return JsonResponse(
                    {"error": "inspection_date must be a valid ISO date (YYYY-MM-DD)."},
                    status=400,
                )
            today = timezone.localdate()
            if new_date < today:
                return JsonResponse(
                    {"error": "Inspection date cannot be in the past."},
                    status=400,
                )
            inspection.inspection_date = new_date

        if "status" in data:
            status = data["status"]
            valid_statuses = {
                Inspection.STATUS_SCHEDULED,
                Inspection.STATUS_PASSED,
                Inspection.STATUS_FAILED,
            }
            if status not in valid_statuses:
                return JsonResponse(
                    {"error": "Status must be one of: scheduled, passed, failed."},
                    status=400,
                )
            inspection.status = status

        if "notes" in data:
            inspection.notes = data["notes"].strip()

        inspection.save()

        return JsonResponse(
            {
                "id": inspection.id,
                "vehicle_plate": inspection.vehicle_plate,
                "inspection_date": inspection.inspection_date.isoformat(),
                "status": inspection.status,
                "notes": inspection.notes,
            }
        )

    return HttpResponseNotAllowed(["GET", "PUT"])


def inspections_page(request):
    """Simple HTML page for optional frontend."""
    return render(request, "inspections/index.html")
