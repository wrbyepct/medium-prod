"""Bookmark signals."""

# ruff: noqa: ANN001, ARG001

from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import BookmarksInCategories, ReadingCategory


@receiver(post_save, sender=BookmarksInCategories)
def increment_bookmark_count(sender, instance, created, **kwargs):
    """Increase 1 count on the newly added bookmark category's boomarks_count."""
    if created:
        ReadingCategory.objects.filter(id=instance.category_id).update(
            bookmarks_count=F("bookmarks_count") + 1
        )


@receiver(post_delete, sender=BookmarksInCategories)
def decrement_bookmark_count(sender, instance, **kwargs):
    """Decrease 1 count on the newly deleted bookmark category's boomarks_count."""
    ReadingCategory.objects.filter(id=instance.category_id).update(
        bookmarks_count=F("bookmarks_count") - 1
    )
