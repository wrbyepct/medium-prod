"""Profile serializer."""

from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Profile Serializer."""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.CharField(source="user.full_name")
    email = serializers.CharField(source="user.email")
    country = CountryField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "gender",
            "country",
            "phone_number",
            "about_me",
            "profile_photo",
            "twitter_handle",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Update Profile serializer."""

    country = CountryField()

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


class FollowingSerializer(serializers.ModelSerializer):
    """Show following user's serializer."""

    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user_full_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
        ]

    def get_user_full_name(self, obj):  # noqa: ANN001
        """Return user full name."""
        return obj.user.full_name
