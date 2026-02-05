from django.urls import path

from . import views

urlpatterns = [
    path("api/inspections", views.inspections_collection, name="inspections_collection"),
    path("api/inspections/<int:id>", views.inspection_detail, name="inspection_detail"),
]

