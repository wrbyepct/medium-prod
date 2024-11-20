"""User form class for admin."""

from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    """User update form."""

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    """User creation form."""

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "email"]
