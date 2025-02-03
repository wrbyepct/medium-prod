import pytest

from core.apps.profiles.models import Profile

pytestmark = pytest.mark.django_db


def test_profile_model_behavior__create_profile_successful(
    profile,
):
    assert profile.user is not None
    assert profile.phone_number == "+8860953127876"
    assert profile.about_me == "Tell others about youself."
    assert profile.gender == "O"
    assert profile.profile_photo.name == "/profile_default.png"
    assert profile.twitter_handle == ""
    assert profile.country == "TW"
    assert profile.city == "London"
    assert profile.followers.all().count() == 0


def test_profile_model_behavior__delete_use_cascades_profile(profile):
    profile_pk = profile.pk
    user = profile.user

    user.delete()
    assert not Profile.objects.filter(pk=profile_pk).exists()


# Test str method
def test_profile_model_behavior__str_method_correct(profile):
    assert profile.__str__() == f"{profile.user.first_name}'s Profile"
