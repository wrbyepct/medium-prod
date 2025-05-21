"""Bookmark Model Manager."""

from django.db import models

from core.apps.articles.models import Article


class ReadingCategoryManager(models.Manager):
    """ReadingCategory manager."""

    def get_queryset(self):
        """Return queryset with annotated field: boomarks_count. Prefetch bookmarks."""
        return (
            super()
            .get_queryset()
            .annotate(bookmarks_count=models.Count("bookmarks", distinct=True))
            .prefetch_related(
                models.Prefetch(
                    "bookmarks", queryset=Article.statistic_objects.preview_data()
                ),
            )
            .order_by("-is_reading_list", "-created_at")
        )
