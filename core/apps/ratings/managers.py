"""Rating Model Manager."""

from django.db import models


class RatingManager(models.Manager):
    """Custom rating manager."""

    def get_queryset(self):
        """Get rating queryset joining table fo user and article."""
        return super().get_queryset().select_related("user", "article")
