"""CustomUser Serializers."""

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.apps.user.managers import CustomUserManager

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Custom User serializer for retrieval.

    Added field from User Profile:
    ------------------------------
        gender
        phone_number
        profile_photo
        country
        city
    """

    gender = serializers.ReadOnlyField(source="profile.gender")
    profile_photo = serializers.ReadOnlyField(source="profile.profile_photo.url")
    city = serializers.ReadOnlyField(source="profile.city")
    phone_number = PhoneNumberField(source="profile.phone_number", read_only=True)
    country = CountryField(source="profile.country", read_only=True)

    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "profile_photo",
            "country",
            "city",
        ]

    def to_representation(self, instance):  # noqa: ANN001
        """Add 'admin' boolean field if the user is superuser."""
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom User serializer for registration.

    Override the RegisterSerializer from dj_rest_auth.
    """

    username = None
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, value: str):
        """Validate email."""
        CustomUserManager.email_validate(value)
        return value

    def get_cleaned_data(self):
        """
        Return the necessary user fields: 'email', 'fist_name', 'last_name', 'password1'.

        Return:
            dict: 'email', 'fist_name', 'last_name', 'password1'

        """
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password1": self.validated_data.get("password1", ""),
        }

    def save(self, request):  # noqa: ANN001
        """Save user with using allauth adapter."""
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        # This code handle saving user into db
        # it access cleaned_data through self.
        # Email normalize happens here
        user = adapter.save_user(request, user, self)
        user.save()

        # This saves user' email to EmailAddress  model from allauth
        # to track if the email is verified or not.
        setup_user_email(request, user, [])

        return user
