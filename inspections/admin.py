from django.contrib import admin

from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("vehicle_plate", "inspection_date", "status")
    list_filter = ("status", "inspection_date")
    search_fields = ("vehicle_plate", "notes")
