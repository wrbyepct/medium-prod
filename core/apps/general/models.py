# mypy: disable-error-code="var-annotated"
"""Abstract Base class: custom TimestampedModel."""

from uuid import uuid4

from django.db import models


class TimestampedModel(models.Model):
    """Abstract base Timstamped base class that uses uuid."""

    pkid = models.BigAutoField(primary_key=True)
    id = models.UUIDField(default=uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Abstract and ordering Meta data."""

        abstract = True
        ordering = ["-created_at", "-updated_at"]
