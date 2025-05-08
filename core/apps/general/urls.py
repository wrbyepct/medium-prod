"""General urls."""

# ruff: noqa: ANN001, ARG002, D301
from django.urls import path

from .views import HealthCheckView

urlpatterns = [path("", HealthCheckView.as_view(), name="api_health")]
