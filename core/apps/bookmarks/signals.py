"""Bookmark signals."""

# ruff: noqa: ANN001, ARG001

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BookmarksInCategories


@receiver(post_save, sender=BookmarksInCategories)
def update_bookmark_count(sender, instance, created, **kwargs):
    """Recalculate a bookmark category's total bookmarks."""
    if created:
        pass
