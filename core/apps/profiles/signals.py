"""Profile model instance auto create via singal."""

import logging
from typing import Literal

from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.bookmarks.models import ReadingCategory
from core.apps.profiles.models import Profile
from core.settings import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


def side_effect(instance):
    """Create user Profile and default ReadingCategory"""
    Profile.objects.create(user=instance)
    logger.info(f"{instance}'s profile has been created.")
    ReadingCategory.objects.create(
        title="Reading list", is_reading_list=True, is_private=True, user=instance
    )
    logger.info(
        f"{instance}'s default 'Reading list' bookmark category has been created."
    )


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Literal["account.User"],
    instance: AbstractBaseUser,
    created: bool,  # noqa: FBT001
    **kwargs: dict,
):
    """Create profile when a user is created."""
    if created:
        side_effect(instance)
