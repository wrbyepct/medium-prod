import pytest
from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core.apps.profiles.models import Profile

User = get_user_model()


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("user", models.OneToOneField),
        ("followers", models.ManyToManyField),
        ("phone_number", PhoneNumberField),
        ("about_me", models.TextField),
        ("gender", models.CharField),
        ("profile_photo", models.ImageField),
        ("twitter_handle", models.CharField),
        ("country", CountryField),
        ("city", models.CharField),
    ],
)
def test_profile_model__field_type_correct(field_name, field_type):
    assert hasattr(Profile, field_name)

    field = Profile._meta.get_field(field_name)
    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        ("phone_number", [("default", "+8860953127876"), ("max_length", 30)]),
        ("about_me", [("default", "Tell others about youself.")]),
        (
            "gender",
            [("choices", Profile.Gender.choices), ("default", Profile.Gender.OTHER)],
        ),
        ("profile_photo", [("default", "/profile_default.png")]),
        ("twitter_handle", [("max_length", 20), ("blank", True)]),
        ("country", [("default", "TW"), ("blank", False), ("null", True)]),
        ("city", [("blank", False), ("default", "London")]),
        (
            "followers",
            [("blank", True)],
        ),  # Blank attr belongs to the field itself, not remote_field
    ],
)
def test_profile_model__simple_field_constraints_correct(field_name, constraints):
    field = Profile._meta.get_field(field_name)
    for attr, value in constraints:
        assert getattr(field, attr) == value


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "user",
            [
                ("model", User),
                ("on_delete", models.CASCADE),
                ("related_name", "profile"),
            ],
        ),
        (
            "followers",
            [
                ("model", Profile),
                ("symmetrical", False),
                ("related_name", "following"),
            ],
        ),
    ],
)
def test_profile_model__remote_field_constraints_correct(field_name, constraints):
    field = Profile._meta.get_field(field_name)
    for attr, value in constraints:
        assert getattr(field.remote_field, attr) == value
