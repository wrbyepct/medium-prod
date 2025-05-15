# mypy: disable-error-code="var-annotated,attr-defined"

"""Profiles models."""

from __future__ import annotations

from functools import partial

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core.apps.general.models import TimestampedModel
from core.tools.image import generate_file_path

upload_to = partial(generate_file_path, app_name="profiles")

User = get_user_model()


class ProfileQuerySet(models.QuerySet):
    """Custom Profile queryset."""

    def join_user_table(self):
        """Return qs by joining table with user."""
        return self.select_related("user")

    def follow_preview_info(self):
        """
        Get only the necessary columns for follower/following info.

        Columns:
           - "profile_photo"
           - "about_me"
           - "twitter_handle"
           - "user__first_name"
           - "user__last_name"

        By selecting joined table from user.
        """
        return (
            self.join_user_table()
            .only(
                "profile_photo",
                "about_me",
                "twitter_handle",
                "user__first_name",
                "user__last_name",
            )
            .order_by("user__first_name")
        )


class ProfileManager(models.Manager):
    """Custom profile manager."""

    def get_queryset(self):
        """Get orignal qs."""
        return ProfileQuerySet(model=self.model, using=self._db)


"""
Fields:
    - Associated User
    - Country(from django-country)
    - Phone Number(from django-phonenumber-field)
    - About me
    - Gender choice(TextChoice class)
    - Profile photo
    - Twitter handle
    - Folloers

Behaviors:
    - Follow
    - Unfollow
    - Check if the user alread exists in my following.

"""


class ProfileFollowMixins:
    """Add follow actions to Profile Model."""

    def follow(self, profile: Profile):
        """Add other Profile instances as followers."""
        self.following.add(profile)

    def unfollow(self, profile: Profile):
        """Remove other Profile instances from followers."""
        self.following.remove(profile)

    def has_followed(self, profile: Profile):
        """Return True if the to-follow-profile has been followed."""
        return self.following.filter(pkid=profile.pkid).exists()


class Profile(TimestampedModel, ProfileFollowMixins):
    """Medium user profile."""

    class Gender(models.TextChoices):
        """Genger text choices class."""

        MALE = "M", _("Male")
        FEMALE = "F", ("Female")
        OTHER = "O", _("Other")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"),
        max_length=30,
        default="+8860953127876",
    )
    about_me = models.TextField(
        verbose_name=_("about me"),
        default="Tell others about youself.",
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    profile_photo = models.ImageField(
        upload_to=upload_to,
        verbose_name=_("profile photo"),
        default="/profile_default.png",
    )
    twitter_handle = models.CharField(
        verbose_name=_("twitter handle"),
        max_length=20,
        blank=True,
    )
    country = CountryField(
        verbose_name=_("country"),
        default="TW",
        blank=False,
        null=True,
    )
    city = models.CharField(
        verbose_name=_("city"),
        blank=False,
        default="London",
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    objects = ProfileManager()

    def __str__(self) -> str:
        """Return string: {self.user.first_name}'s Profile."""
        return f"{self.user.first_name}'s Profile"
