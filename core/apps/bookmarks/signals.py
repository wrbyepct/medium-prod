"""Bookmark signals."""

# ruff: noqa: ANN001, ARG001
import logging

from django.db import IntegrityError
from django.db.models import F
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .exceptions import SignalProcessingError
from .models import ReadingCategory

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=ReadingCategory.bookmarks.through)
def increment_bookmark_count(
    sender, instance: ReadingCategory, action, pk_set, **kwargs
):
    """Increase 1 count on the newly added bookmark category's boomarks_count."""
    # pk_set will have items, if unique items are added to the m2m field.
    if action == "post_add" and pk_set:
        ReadingCategory.objects.filter(id=instance.id).update(
            bookmarks_count=F("bookmarks_count") + 1
        )
        instance.refresh_from_db()  # update new count status


@receiver(m2m_changed, sender=ReadingCategory.bookmarks.through)
def decrement_bookmark_count(
    sender, instance: ReadingCategory, action, pk_set, **kwargs
):
    """Decrease 1 count on the newly deleted bookmark category's boomarks_count."""
    if action == "post_remove":
        try:
            ReadingCategory.objects.filter(id=instance.id).update(
                bookmarks_count=F("bookmarks_count") - 1
            )
            instance.refresh_from_db()
        except IntegrityError:
            logger.exception(
                msg="Error occurred when trying to subtract a ReadingCategory's bookmarks_count."
            )
            raise SignalProcessingError  # noqa: B904
