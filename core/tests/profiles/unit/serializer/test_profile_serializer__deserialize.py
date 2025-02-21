import pytest

from core.apps.profiles.serializers import FollowingSerializer, ProfileSerializer

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.unit,
    pytest.mark.profile(type="serializer"),
]

"""
Test ProfileSerializer & FollowerSerializer for serialize only 
Because they are only used in representation.
"""


# Test ProfileSerializer
class TestProfileSerialize:
    def test_profile_serializer__serialize_correct(self, profile):
        serializer = ProfileSerializer(profile)
        fields = ProfileSerializer.Meta.fields

        data = serializer.data
        # Assert profile data
        for field in fields:
            assert field in data

        profile_fields = [
            "gender",
            "country",
            "phone_number",
            "about_me",
            "twitter_handle",
        ]
        for field in profile_fields:
            assert data[field] == getattr(profile, field)
        assert data["id"] == str(profile.id)
        assert data["profile_photo"] == profile.profile_photo.url

        # Assert user data
        user_fields = [
            "first_name",
            "last_name",
            "full_name",
            "email",
        ]
        user = profile.user
        for field in user_fields:
            assert data[field] == getattr(user, field)

    # Test FollowingSerializer
    def test_profile_serializer__follower_serialize_correct(self, profile):
        serializer = FollowingSerializer(profile)
        fields = FollowingSerializer.Meta.fields

        data = serializer.data
        for field in fields:
            assert field in data

        assert data["user_full_name"] == profile.user.full_name
        assert data["profile_photo"] == profile.profile_photo.url
        assert data["about_me"] == profile.about_me
        assert data["twitter_handle"] == profile.twitter_handle
