# mypy: disable-error-code="var-annotated,attr-defined"

"""Profiles models."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core.apps.general.models import TimestampedModel

User = get_user_model()

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
    - Check follower exists.

"""


class Profile(TimestampedModel):
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
        default="Lundon",
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self) -> str:
        """Return string: {self.user.first_name}'s Profile."""
        return f"{self.user.first_name}'s Profile"

    def follow(self, profile: Profile):
        """Add other Profile instances as followers."""
        self.following.add(profile)

    def unfollow(self, profile: Profile):
        """Remove other Profile instances from followers."""
        self.following.remove(profile)

    def has_followed(self, profile: Profile):
        """Return True if the follower id in check exists in current followers."""
        return self.following.filter(pkid=profile.pkid).exists()
