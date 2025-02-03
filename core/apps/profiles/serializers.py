"""Profile serializer."""

from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class BaseProfileSerializer(serializers.ModelSerializer):
    """Base Profile serializer."""

    country = CountryField()

    def to_representation(self, instance: Profile):
        """Return image relative url instead of absolute."""
        data = super().to_representation(instance)
        data["profile_photo"] = instance.profile_photo.url
        return data

    class Meta:
        model = Profile
        fields = [
            "gender",
            "country",
            "phone_number",
            "about_me",
            "profile_photo",
            "twitter_handle",
        ]


class ProfileSerializer(BaseProfileSerializer):
    """Profile Serializer."""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.CharField(source="user.full_name")
    email = serializers.CharField(source="user.email")

    class Meta(BaseProfileSerializer.Meta):
        fields = [
            *BaseProfileSerializer.Meta.fields,
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
        ]


class UpdateProfileSerializer(BaseProfileSerializer):
    """Update Profile serializer."""


class FollowingSerializer(serializers.ModelSerializer):
    """Show following user's serializer."""

    user_full_name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user_full_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
        ]
        read_only_fields = [
            "about_me",
            "twitter_handle",
        ]

    def get_profile_photo(self, obj: Profile):
        """Return relative path."""
        return obj.profile_photo.url

    def get_user_full_name(self, obj):  # noqa: ANN001
        """Return user full name."""
        return obj.user.full_name
